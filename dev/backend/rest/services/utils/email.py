import string

from django.core.mail import send_mail
from django.utils.crypto import random


class EmailService:
    def __init__(self):
        pass

    @staticmethod
    def get_email_confirmation_message(request, cookie=None):
        host = request.META['SERVER_NAME'] + ':3000/#'  # TODO. Not for production.
        # host = request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT']
        message = 'Please confirm your account at upMoodle.\n'
        message += 'http://' + host + '/confirm_email/' + cookie
        return message

    @staticmethod
    def get_password_recover_message(password):
        message = 'In theory, you\'ve forgotten your password.\n'
        message += 'This is your new password: ' + password + '\n'
        message += 'For security reasons, please, change this password as soon as possible.'
        return message

    @staticmethod
    def send_email(subject, message, receivers):
        send_mail(subject, message, 'info@upmoodle.com', receivers, fail_silently=False)

    @staticmethod
    def send_recover_password_email(email, password):
        subject = 'Password recovery'
        message = EmailService.get_password_recover_message(password)
        EmailService.send_email(subject, message, [email])

    @staticmethod
    def get_random_email():
        length = 10
        email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return email + '@upm.es'
