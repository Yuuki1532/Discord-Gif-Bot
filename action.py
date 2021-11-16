import logging
import utils

logger = logging = logging.getLogger('__main__')

@utils.no_db
async def help(message, *args):
    await message.channel.send('```Usage: !help | !echo TEXT | !show TAGS ... | !add TAGS ... URL```')

@utils.no_db
async def echo(message, *text):
    if len(text) == 0:
        logger.info(f'Text is empty in command "echo"')
        await message.channel.send('What do you want me to say?')
        return

    text = ' '.join(text)
    logger.info(f'Send message: "{text}"')
    await message.channel.send(text)



async def show(message, db, *tags):
    if len(tags) == 0:
        logger.info(f'Tag is empty in command "show"')
        await message.channel.send('Tag cannot be empty.')
        return

    # query cached db
    url = db.cached_get_url(*tags)

    if url is None:
        logger.info(f'Cannot find an unique match in command "show"')
        await message.channel.send('Cannot find an unique match.')
        return

    logger.info(f'Send message: "{url}"')
    await message.channel.send(url)

    pass

async def ls(message, db):
    pass

async def add(message, db, *args):
    if len(args) < 2:
        logger.info(f'Tag and/or url is empty in command "add"')
        await message.channel.send('At least one tag should be provided along with an url.')
        return

    tags, url = args[:-1], args[-1]



    pass

async def rm(message):
    pass




