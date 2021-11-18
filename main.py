import os
import argparse
import logging
import dotenv
from client import BotClient
from db import GSheetClient

# set up logger
logger = logging.getLogger('__main__')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--loglevel',
        type=str,
        default='debug',
        help='Provide logging level. For example, --loglevel debug',
    )

    args = parser.parse_args()

    # set loggin config
    logging.basicConfig(
        format='{asctime} [{levelname}] {message}',
        style='{',
        level=args.loglevel.upper(),
    )

    # import env vars from .env file
    dotenv.load_dotenv()
    logger.debug('Env vars have been imported from .env')

    # set up gsheet client as db
    gsheet_client = GSheetClient()

    # create and start bot client with all intents
    client = BotClient(gsheet_client)

    client.run(os.getenv('BOT_TOKEN'))


