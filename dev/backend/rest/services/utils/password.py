import string
from random import randrange
from django.utils.crypto import random


class PasswordService:
    def __init__(self):
        pass

    @staticmethod
    def get_random():
        password_length = randrange(10, 20)
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(password_length))
