import os
import logging
from googleapiclient import discovery
from google.oauth2 import service_account

logger = logging.getLogger('__main__')

class GSheetClient:

    @staticmethod
    def parse_row(row):
        # parse a row (list, without its index) to a dict with each key=column_name, value=value_of_column
        return {
            'uploader': row[0],
            'nickname': row[1],
            'content': row[2],
            'tags': row[3:],
        }

    def __init__(self):

        self._header_lines = 1

        key_file_path = os.getenv('SERVICE_ACCOUNT_KEY_FILE')

        if not os.path.exists(key_file_path):
            logger.error(f'Key file {key_file_path} for gsheet service account auth does not exist')
            raise Exception(f'Key file {key_file_path} for gsheet service account auth does not exist')

        self._creds = service_account.Credentials.from_service_account_file(key_file_path)
        logger.debug('Credentials from service account file loaded')

        self._sheet_id = os.getenv('SHEET_ID')
        self._service = discovery.build('sheets', 'v4', credentials=self._creds)
        logger.info('Services for gsheet has built')

        self._cache = None # maintain a cached local copy to avoid waiting for each API call

        self.update_cache()

        self.create_lookup_tables()


    def update_cache(self):
        logger.info('Start updating local cache')

        sheet = self._gsheet_get("'content_db'")

        if sheet is None:
            logger.warning('Retrieved gsheet is empty')
            logger.warning('Failed to update cache')
            return

        # empty cache
        self._cache = {}
        logger.info(f'Empty cache')


        # ignore header lines
        sheet = sheet[self._header_lines:]

        # iterate over cells
        for r in range(len(sheet)):
            # read a row
            id_, *data = sheet[r]
            # add a new row (by its id)
            self._cache[id_] = data
            logger.debug(f'Added {" ".join(sheet[r])}')

        logger.info(f'Added {len(sheet)} rows to cache')



        logger.info('Finished updating local cache')
        pass

    def create_lookup_tables(self):
        # create lookup tables for uploader names and tags

        logger.info(f'Creating lookup tables for fast searching')

        uploader_dict = {}
        nickname_dict = {}
        tag_dict = {}

        for id_, data in self._cache.items():
            values = self.parse_row(data)
            uploader, nickname, content, tags = values['uploader'], values['nickname'], values['content'], values['tags']

            # uploader
            uploader_set = uploader_dict.setdefault(uploader, set())
            uploader_set.add(id_)

            # nickname
            nickname_set = nickname_dict.setdefault(nickname, set())
            nickname_set.add(id_)

            # tags
            for tag in tags:
                tag_set = tag_dict.setdefault(tag, set())
                tag_set.add(id_)


        self._uploader_dict = uploader_dict
        self._nickname_dict = nickname_dict
        self._tag_dict = tag_dict

        logger.info(
            f'Lookup tables created with {len(uploader_dict)} unique uploader names, '
            f'{len(nickname_dict)} unique nicknames, '
            f'{len(tag_dict)} unique tags')


    def cached_search(self, *tags, uploader=None, nickname=None):
        # search and return the list of matched id(s) from the given parameters

        search_dicts = []


        if len(tags) > 0:

            # special case which inputs id directly
            for tag in tags:
                if tag in self._cache:
                    logger.info(f'Matched by id')
                    return [tag]

            tag_dicts = [self._tag_dict[tag] for tag in tags if tag in self._tag_dict]
            search_dicts.extend(tag_dicts)

        if uploader is not None:
            if uploader in self._uploader_dict:
                search_dicts.append(self._uploader_dict[uploader])

        if nickname is not None:
            if nickname in self._nickname_dict:
                search_dicts.append(self._nickname_dict[nickname])


        if len(search_dicts) == 0:
            return []


        intersection_id_set = set.intersection(*search_dicts)

        return list(intersection_id_set)


    def cached_getdata(self, index) -> dict:
        # return the parsed row of index
        if index in self._cache:
            return self.parse_row(self._cache[index])

        # logger.warning('A nonexist index is given to retrieve data from local cache')
        return None

    def adddata(self, index, *data):

        if index in self._cache:
            logger.warning(f'Attempt to add an exist id to local cache, ignored')
            return

        # add entry to local cache
        self._cache[index] = list(data)
        logger.debug(f'Row added to cache with id: {index}')

        # update lookup table
        logger.debug(f'Updating lookup table')

        values = self.parse_row(data)
        uploader, nickname, content, tags = values['uploader'], values['nickname'], values['content'], values['tags']

        # uploader
        uploader_set = self._uploader_dict.setdefault(uploader, set())
        uploader_set.add(index)

        # nickname
        nickname_set = self._nickname_dict.setdefault(nickname, set())
        nickname_set.add(index)

        # tags
        for tag in tags:
            tag_set = self._tag_dict.setdefault(tag, set())
            tag_set.add(index)

        # send to remote
        logger.debug(f'Sending to remote')
        self._gsheet_append(index, *data, search_range="'content_db'")

        logger.info(f'Row added with id: {index}')


    def _gsheet_get(self, range):
        logger.debug('Getting gsheet in range: {range}')

        response = self._service.spreadsheets().values().get(spreadsheetId=self._sheet_id, range=range).execute()
        return response.get('values', None)

    def _gsheet_append(self, *data, search_range):
        # append a single new row to gsheet
        # search range: range of the table, in order to find the row number to append

        logger.debug('Appending a new row to gsheet')

        body = {
            'majorDimension': 'ROWS',
            'values': [
                list(data)
            ]
        }

        response = self._service.spreadsheets().values().append(
            spreadsheetId=self._sheet_id,
            range=search_range,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body,
        ).execute()

        logger.info('Successfully appended a new row to gsheet')
        return


