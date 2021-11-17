import logging
import asyncio
import discord
import action

logger = logging = logging.getLogger('__main__')
MAX_MSG_PRINT_LEN = 50

class BotClient(discord.Client):
    def __init__(self, gsheet_client):
        super().__init__()
        self.prefix = '!'
        self._gsheet_client = gsheet_client

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        logger.info(f'{self.user} has connected to Discord')

    async def on_message(self, message):
        logger.debug(f'Received message: "{message.clean_content[:MAX_MSG_PRINT_LEN]}" from {message.author.display_name} ({message.author.name}#{message.author.discriminator}) @ {message.guild.name}#{message.channel.name}')

        if message.author == self.user:
            return

        content = message.content.strip()

        if not content.startswith(self.prefix): # no need to handle
            return

        # remove prefix
        content = content[len(self.prefix):]

        if len(content) <= 0:
            return

        logger.debug(f'Received a valid message, start parsing')

        # tokenize
        cmd, *args = content.split()

        # try to find a function to handle
        cmd_exec = getattr(action, cmd, None)

        if cmd_exec is not None and callable(cmd_exec):
            logger.info(f'Executing command: "{cmd}" with args {args}')
            asyncio.create_task(cmd_exec(message, self._gsheet_client, *args)) # we still need the reference to the message object however

        else:
            logger.info(f'Received unknown command: {cmd}')

            # shortcut
            logger.info(f'Treat as shortcut: !show {cmd} {" ".join(args)}')
            asyncio.create_task(action.show(message, self._gsheet_client, cmd, *args, suppress_warning=True))


