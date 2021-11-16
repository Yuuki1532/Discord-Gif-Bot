import os
import logging
import json
from googleapiclient import discovery
from google.oauth2 import service_account

logger = logging.getLogger('__main__')

class GSheetClient:
    def __init__(self):
        if not os.path.exists('key.json'):
            logger.error('Currently need key.json file for gsheet auth')
            raise NotImplemented('Currently need key.json file for gsheet auth')

        self._creds = service_account.Credentials.from_service_account_file('key.json')
        logger.debug('Credentials from service account file loaded')

        self._sheet_id = os.getenv('SHEET_ID')
        self._service = discovery.build('sheets', 'v4', credentials=self._creds)
        logger.info('Services for gsheet has built')

        self._cache = None # maintain a cached local copy to avoid waiting for each API call

        self.update_cache()


    def update_cache(self):
        sheet = self.get("'gif_db'")

        if sheet is None:
            logger.warning('Retrieved gsheet is empty')
            logger.warning('Failed to update cache')
            return


        logger.debug('Finished updating local cache')
        pass

    def get(self, range):
        logger.debug('Getting gsheet in range: {range}')

        response = self._service.spreadsheets().values().get(spreadsheetId=self._sheet_id, range=range).execute()
        return response.get('values', None)

    def set(self, range, value):
        pass


