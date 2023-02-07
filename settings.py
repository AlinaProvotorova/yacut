import os
import re
from string import ascii_letters, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', '123qwe')


MAX_SIZE_SHORT = 6
MAX_SIZE_URL = 2048
MAX_SIZE_SHORT_FOR_USER = 16
VALID_CHARACTERS = ascii_letters + digits
PATTERN_VALID_CHARACTERS = fr'^[{re.escape(VALID_CHARACTERS)}]+$'
MAX_COUNT_GET_UNIQUE_SHORT = 10
