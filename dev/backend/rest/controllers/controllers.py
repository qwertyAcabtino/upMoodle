import calendar
import datetime
import string
from random import randrange

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils.crypto import random

from backend.settings import SESSION_COOKIE_NAME_BIS
from rest.MESSAGES_ID import INCORRECT_DATA, DISABLED_COOKIES, NOT_SIGNED_IN, REQUEST_CANNOT, UNAUTHORIZED
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.models import User


def get_email_confirmation_message(request, cookie=None):
    host = request.META['SERVER_NAME'] + ':3000/#'  # TODO. Not for production.
    # host = request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT']
    message = 'Please confirm your account at upMoodle.\n'
    message += 'http://' + host + '/confirm_email/' + cookie
    return message


def get_password_recover_message(password):
    message = 'In theory, you\'ve forgotten your password.\n'
    message += 'This is your new password: ' + password + '\n'
    message += 'For security reasons, please, change this password as soon as possible.'
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
    return len(request.COOKIES) != 0 and request.COOKIES[SESSION_COOKIE_NAME_BIS] \
           and not len(request.COOKIES[SESSION_COOKIE_NAME_BIS]) == 0


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
    """
    :param request: here comes the information for the signed user.
    :param author_id: original author of the information.
    :param level: check the hierarchy. If the signed user has a lower value, exception is raised
    :param same: checks if the user that is trying to push changes is the same than the original.
    :return:
    """

    userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME_BIS])
    userAuthor = User.objects.get(id=author_id)
    rolAuthor = userAuthor.rol
    rolSigned = userSigned.rol
    if same and not author_id == userSigned.id:
        raise RequestExceptionByCode(UNAUTHORIZED)
    elif level and rolSigned.priority < rolAuthor.priority:
        raise RequestExceptionByCode(UNAUTHORIZED)


def is_valid_month_initDate(initDate):
    values = initDate.split('-')
    return 0 < int(values[1]) < 13 and 2010 < int(values[0]) < 2100


def is_valid_day_initDate(initDate):
    try:
        datetime.datetime.strptime(initDate, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_initDate_by_period(period, initDate):
    try:
        validDate = True
        if period == "month":
            validDate = is_valid_month_initDate(initDate)
        elif period == "day":
            validDate = is_valid_day_initDate(initDate)
        if not validDate:
            raise RequestExceptionByCode(INCORRECT_DATA)
        else:
            return True
    except ValueError:
        raise RequestExceptionByCode(INCORRECT_DATA)


def get_date_range(period, initDate):
    DATE_FORMAT = '%Y-%m-%d'
    values = initDate.split('-')
    day = int(values[2]) if period == "day" else 1
    date = datetime.datetime(int(values[0]), int(values[1]), day)
    rangeStart = date.strftime(DATE_FORMAT)
    if period == "day":
        return [rangeStart, rangeStart]
    else:
        monthsDays = calendar.monthrange(date.year, date.month)[1] - 1
        rangeEnd = (date + datetime.timedelta(monthsDays)).strftime(DATE_FORMAT)
    return [rangeStart, rangeEnd]
