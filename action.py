import logging
import asyncio
import utils
import uuid

logger = logging = logging.getLogger('__main__')

cache_update_otp = None

@utils.no_db
async def help(message, *args):
    await message.channel.send(
        '```Usage:\n'
        '\t!help |\n'
        '\t!echo CONTENT |\n'
        '\t!show [ID] [TAGS ...] |\n'
        '\t!ls [TAGS ...] [uploader=UPLOADER] [nickname=NICKNAME] |\n'
        '\t!add [TAGS ...] CONTENT```'
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



async def show(message, db, *tags, suppress_warning=False):
    if len(tags) == 0:
        logger.info(f'Tag is empty in command "show"')
        if not suppress_warning:
            await message.channel.send('Tag cannot be empty.')
        return

    # case insensitive (lower case always)
    tags = [tag.lower() for tag in tags]

    # query cached db
    ids = db.cached_search(*tags)

    if len(ids) != 1:
        logger.info(f'Cannot find an unique match in command "show"')
        if not suppress_warning:
            await message.channel.send('Cannot find an unique match.')
        return

    content = db.cached_getdata(ids[0])[2]
    logger.info(f'Send message: "{content}"')
    await message.channel.send(content)

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
        logger.info(f'Tag and/or content is empty in command "add"')
        await message.channel.send('At least one tag should be provided along with the content.')
        return

    tags, content = args[:-1], args[-1]

    # check duplicate
    id_ = utils.get_str_hash(content)

    if db.cached_getdata(id_) is not None:
        logger.info(f'Attempt to add an exist row with id: {id_} in command "add"')
        await message.channel.send('The given content has already been added to the database.')
        return

    db.adddata(id_, message.author.name, message.author.display_name, content, *tags)
    await message.channel.send('Success!')


async def rm(message):
    pass

async def request_cache_update(message, db):
    global cache_update_otp

    async def delete_cache_update_otp(expire_time=20):
        global cache_update_otp
        await asyncio.sleep(expire_time)
        cache_update_otp = None

    cache_update_otp = uuid.uuid4().hex
    logger.warning(f'Received request for cahce update. OTP: {cache_update_otp}')
    await message.channel.send('Please provide the OTP showed on the debug console by `confirm_cache_update OTP`')

    # delete otp after it expires
    asyncio.create_task(delete_cache_update_otp())

async def confirm_cache_update(message, db, otp):
    global cache_update_otp

    if cache_update_otp is None:
        logger.warning('OPT not requested or expired for cache update')
        await message.channel.send('OPT not requested or expired for cache update.')
        return

    if otp == cache_update_otp:
        logger.warning(f'Received OTP accepted. Updating local cache')
        cache_update_otp = None
        db.update_cache()
        db.create_lookup_tables()
    else:
        logger.warning(f'Received OTP rejected.')
        await message.channel.send('OPT rejected.')
        return

    await message.channel.send('Success!')

