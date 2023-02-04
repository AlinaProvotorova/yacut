from string import ascii_letters, digits

MAX_SIZE_SHORT = 6
MAX_SIZE_SHORT_FOR_USER = 16
MAX_SIZE_URL = 256
VALID_CHARACTERS = ascii_letters + digits
MAX_COUNT = len(VALID_CHARACTERS) ** MAX_SIZE_SHORT
