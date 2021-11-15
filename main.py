import os
import argparse
import logging
import dotenv
from client import BotClient
# from db import GSheetClient

# set up logger
logger = logging.getLogger('__main__')

# import env vars from .env file
dotenv.load_dotenv()
logging.debug('Env vars have been imported from .env')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-log',
        '--loglevel',
        type=str,
        default='debug',
        help='Provide logging level. For example, --loglevel debug',
    )

    args = parser.parse_args()

    logging.basicConfig(
        format='{asctime} [{levelname}] {message}',
        style='{',
        level=args.loglevel.upper(),
    )

    client = BotClient()
    logging.info('Client object created')

    client.run(os.getenv('BOT_TOKEN'))
    logging.info('Client has started running')

    pass
