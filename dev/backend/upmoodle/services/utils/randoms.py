import string
from random import randrange
from django.utils.crypto import random


class RandomStringsService:
    def __init__(self):
        pass

    @staticmethod
    def _random_string(length):
        return (random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def random_password():
        password_length = randrange(10, 20)
        return ''.join(RandomStringsService._random_string(password_length))

    @staticmethod
    def random_email():
        length = 10
        email = ''.join(RandomStringsService._random_string(length))
        return email + '@upm.es'
