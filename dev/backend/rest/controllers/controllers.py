import datetime
from random import randrange
import string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.crypto import random
from backend.settings import SESSION_COOKIE_NAME, SESSION_COOKIE_NAME_BIS
from rest.MESSAGES_ID import INCORRECT_DATA, DISABLED_COOKIES, NOT_SIGNED_IN, REQUEST_CANNOT, UNAUTHORIZED
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.models import User


def get_email_confirmation_message(request):
    cookie = request.COOKIES[SESSION_COOKIE_NAME_BIS]
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


def get_random_email():
    length = 10
    email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    return email + '@upm.es'


def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def cookies_are_ok(request):
    try:
        return request.COOKIES[SESSION_COOKIE_NAME_BIS] \
               and not len(request.COOKIES[SESSION_COOKIE_NAME_BIS]) == 0
    except KeyError:
        return request.COOKIES[SESSION_COOKIE_NAME] \
               and not len(request.COOKIES[SESSION_COOKIE_NAME]) == 0
    # return request.session.test_cookie_worked() \
    #        and request.COOKIES[SESSION_COOKIE_NAME_BIS] \
    #        and not len(request.COOKIES[SESSION_COOKIE_NAME_BIS]) == 0


def is_signed_in(request):
    try:
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME_BIS]
        user = User.objects.get(sessionToken=sessionToken)
        if user.banned:
            return False
        else:
            return True
    except ObjectDoesNotExist:
        return False
    except KeyError as k:
        return False


def check_cookies(request):
    if not cookies_are_ok(request):
        raise RequestExceptionByCode(DISABLED_COOKIES)


def check_signed_in(request):
    if not is_signed_in(request):
        raise RequestExceptionByCode(NOT_SIGNED_IN)


def check_request_method(request, method):
    if not request.method == method:
        raise RequestExceptionByCode(REQUEST_CANNOT)


def check_signed_in_request(request, *args, **kwargs):
    check_cookies(request)
    check_signed_in(request)
    method = kwargs.get('method', None)
    if method:
        check_request_method(request, method)


def check_authorized_author(request, author_id, level=False, same=True):
    # TODO. Level.
    userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME_BIS])
    if same and not author_id == userSigned.id:
        raise RequestExceptionByCode(UNAUTHORIZED)