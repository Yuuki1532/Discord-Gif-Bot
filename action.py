import logging
import utils

logger = logging = logging.getLogger('__main__')

@utils.no_db
async def help(message, *args):
    await message.channel.send(
        '```Usage:\n'
        '\t!help |\n'
        '\t!echo TEXT |\n'
        '\t!show [ID] [TAGS ...] |\n'
        '\t!ls [TAGS ...] [uploader=UPLOADER] [nickname=NICKNAME]```'
        )

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

    # case insensitive (lower case always)
    tags = [tag.lower() for tag in tags]

    # query cached db
    ids = db.cached_search(*tags)

    if len(ids) != 1:
        logger.info(f'Cannot find an unique match in command "show"')
        await message.channel.send('Cannot find an unique match.')
        return

    url = db.cached_getdata(ids[0])[2]
    logger.info(f'Send message: "{url}"')
    await message.channel.send(url)

    pass

async def ls(message, db, *args):
    if len(args) == 0:
        logger.info(f'Filter is empty in command "ls"')
        await message.channel.send('Filter cannot be empty. (complete ls is not supported)')
        return

    tags, uploader, nickname = [], None, None

    for arg in args:
        if arg.startswith('uploader='):
            uploader = arg.split('=', maxsplit=1)[-1]
        elif arg.startswith('nickname='):
            nickname = arg.split('=', maxsplit=1)[-1]
        else:
            tags.append(arg.lower())
    
    # query cached db
    ids = db.cached_search(*tags, uploader=uploader, nickname=nickname)

    if len(ids) == 0:
        logger.info(f'Cannot find any match in command "ls"')
        await message.channel.send('Cannot find any match.')
        return

    output = ''

    for id_ in ids:
        row = db.cached_getdata(id_)
        output += f'```{id_} {" ".join(row)}```'

    logger.info(f'{len(ids)} rows found')
    await message.channel.send(f'{len(ids)} row(s) found.\n{output}')

async def add(message, db, *args):
    if len(args) < 2:
        logger.info(f'Tag and/or url is empty in command "add"')
        await message.channel.send('At least one tag should be provided along with an url.')
        return

    tags, url = args[:-1], args[-1]



    pass

async def rm(message):
    pass




