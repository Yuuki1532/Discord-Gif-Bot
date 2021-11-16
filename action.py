import logging

logger = logging = logging.getLogger('__main__')

async def help(message, *args):
    await message.channel.send('```Usage: !help | !echo TEXT | !show TAGS ...```')

async def show(message, *tags):
    if len(tags) == 0:
        logger.info(f'Tag is empty in command "show"')
        await message.channel.send('Tag cannot be empty.\n```Usage: !show tag1[tag2[tag3...]]```')
        return


    pass

async def add(message):
    pass

async def delete(message):
    pass

async def echo(message, *text):
    if len(text) == 0:
        logger.info(f'Text is empty in command "echo"')
        await message.channel.send('What do you want me to say?')
        return

    text = ' '.join(text)
    logger.info(f'Echoed message: "{text}"')
    await message.channel.send(text)


