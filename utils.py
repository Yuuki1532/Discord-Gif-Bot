import logging
import hashlib

logger = logging = logging.getLogger('__main__')

def no_db(func):
    def wrapper(message, db, *args):
        return func(message, *args)
    return wrapper

def get_str_hash(str_):
    return hashlib.sha256(str_.encode()).hexdigest()
