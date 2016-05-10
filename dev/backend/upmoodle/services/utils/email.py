from django.core.mail import send_mail

from backend import settings


class EmailService:
    def __init__(self):
        pass

    @staticmethod
    def _get_email_confirmation_message(session_token=None):
        host = settings.DOMAIN + ':3000/#'
        message = 'Please confirm your account at upMoodle.\n'
        message += 'http://' + host + '/confirm_email/' + session_token
        return message

    @staticmethod
    def _get_password_recover_message(password):
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
        message = EmailService._get_password_recover_message(password)
        EmailService.send_email(subject, message, [email])

    @staticmethod
    def send_signup_confirmation_email(email=None, session_token=None):
        subject = 'Email confirmation'
        message = EmailService._get_email_confirmation_message(session_token=session_token)
        EmailService.send_email(subject, message, [email])
