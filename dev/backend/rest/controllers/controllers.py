import datetime
from random import randrange
import string
from django.core.mail import send_mail
from django.utils.crypto import random
from backend.settings import SESSION_COOKIE_NAME


def get_email_confirmation_message(request):
    cookie = request.COOKIES[SESSION_COOKIE_NAME]
    host = request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT']
    message = 'Please confirm your account at upMoodle.\n'
    message += 'http://' + host + '/confirm_email/' + cookie
    return message


def get_password_recover_message(password):
    message = 'In theory, you\'ve forgotten your password.\n'
    message += 'This is your new password: ' + password + '\n'
    message += 'For security reasons, please, change this password as soon as posible.'
    return message


def send_email(subject, message, receivers):
    send_mail(subject, message, 'info@upmoodle.com', receivers, fail_silently=False)


def send_recover_password_email(email, password):
    subject = 'Password recovery'
    message = get_password_recover_message(password)
    send_email(subject, message, [email])


def get_random_password():
    passwordLength = randrange(10, 20)
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(passwordLength))
    return password


def cookies_are_ok(request):
    return request.session.test_cookie_worked() \
           and request.COOKIES[SESSION_COOKIE_NAME] \
           and not len(request.COOKIES[SESSION_COOKIE_NAME]) == 0