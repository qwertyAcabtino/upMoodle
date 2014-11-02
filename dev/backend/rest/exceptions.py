#ERRORS
REQUEST_CANNOT = 1
INCORRECT_DATA = 2
DISABLED_COOKIES = 3
ALREADY_CONFIRMED = 4
INVALID_TOKEN = 5
USER_IN_USE = 6
UNAUTHORIZED = 7
INCORRECT_FILE_DATA = 8
PASSWORD_LENGTH = 9
NICK_LENGTH = 10

class ExtensionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)