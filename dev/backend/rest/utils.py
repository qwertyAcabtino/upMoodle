from backend.settings import SESSION_COOKIE_NAME


def get_email_confirmation_message(request):
    cookie = request.COOKIES[SESSION_COOKIE_NAME]
    host = request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT']
    message = 'Please confirm your account at upMoodle.\n'
    message += 'http://' + host + '/confirm_email/' + cookie
    return message