import discord
import logging

logger = logging = logging.getLogger('__main__')
MAX_MSG_PRINT_LEN = 50

class BotClient(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        logging.info(f'{self.user} has connected to Discord')

    async def on_message(self, message):
        logger.debug(f'Received message: "{message.clean_content[:MAX_MSG_PRINT_LEN]}" from {message.author.display_name} ({message.author.name}) @ {message.guild.name}#{message.channel.name}')


