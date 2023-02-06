import os
from string import ascii_letters, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', '123qwe')


MAX_SIZE_SHORT = 6
MAX_SIZE_SHORT_FOR_USER = 16
VALID_CHARACTERS = ascii_letters + digits
PATTERN_VALID_CHARACTERS = r'^[A-Za-z0-9]+$'
PATTERN_VALID_URL = r'(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$'
MAX_COUNT_CREATE_SHORT = len(VALID_CHARACTERS) ** MAX_SIZE_SHORT - 1
