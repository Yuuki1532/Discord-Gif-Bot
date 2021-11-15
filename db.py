import os.path
import logging
from googleapiclient import discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger('__main__')

class GSheetClient:
    def __init__(self):
        if not os.path.exists('token.json'):
            raise NotImplemented('Currently need token.json file for auth')

        self._creds = Credentials.from_authorized_user_file('token.json')
        logging.info('[I] Credentials')
        self._sheet_id = None # TODO: get from env var
        self._service = discovery.build('sheets', 'v4', credentials=creds)

    def get(self):
        
        pass



