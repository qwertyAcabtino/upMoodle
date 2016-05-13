import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from backend.settings import SESSION_COOKIE_NAME
from upmoodle.controllers.decorators.exceptions import map_exceptions
from upmoodle.models import User
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.services.utils.email import EmailService
from upmoodle.services.utils.randoms import RandomStringsService


class AuthService:

    def __init__(self):
        pass

    @staticmethod
    def get_cookie(session_token):
        if not session_token:
            return uuid.uuid4().hex
        else:
            return session_token

    @staticmethod
    @map_exceptions
    def login(session_token=None, data=None):
        session_token = AuthService.get_cookie(session_token)

        request_email = data['email']
        request_pass = data['password']
        user = User.objects.get(email=request_email, password=request_pass)
        if not user.confirmedEmail:
            raise MessageBasedException(message_id=ErrorMessage.Type.UNCONFIRMED_EMAIL)
        else:
            user.sessionToken = session_token
            user.lastTimeActive = timezone.now()
            user.save()
            return {SESSION_COOKIE_NAME: session_token}

    @staticmethod
    @map_exceptions
    def signup(session_token=None, data=None):
        session_token = AuthService.get_cookie(session_token)

        user = User.parse(data, sessionToken=session_token, fields=['email', 'password', 'nick', 'name'])
        EmailService.send_signup_confirmation_email(email=user.email, session_token=session_token)
        user.save()
        return {SESSION_COOKIE_NAME: session_token}

    @staticmethod
    @map_exceptions
    def logout(session_token=None):
        session_token = AuthService.get_cookie(session_token)
        user = User.objects.get(sessionToken=session_token)
        user.sessionToken = ''
        user.save()
        return {SESSION_COOKIE_NAME: ''}

    @staticmethod
    @map_exceptions
    def confirm_email(session_token=None):
        user = User.objects.get(sessionToken=session_token)
        if user.confirmedEmail:
            raise MessageBasedException(message_id=ErrorMessage.Type.ALREADY_CONFIRMED)
        else:
            user.confirmedEmail = True
            user.save()

    @staticmethod
    @map_exceptions
    def recover_password(data=None):
        email_request = data['email']
        user = User.objects.get(email=email_request)
        if not user.confirmedEmail:
            raise MessageBasedException(message_id=ErrorMessage.Type.UNCONFIRMED_EMAIL)
        elif user.banned:
            raise MessageBasedException(message_id=ErrorMessage.Type.UNAUTHORIZED)
        else:
            password = RandomStringsService.random_password()
            EmailService.send_recover_password_email(user.email, password)
            user.password = password
            user.save()

    @staticmethod
    def is_authenticated(session_token):
        try:
            user = User.objects.get(sessionToken=session_token)
            if user.banned:
                return False
            else:
                return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def is_authorized_author(session_token=None, author_id=None, level=False, same=True):
        """
        :param session_token: authentication token
        :param author_id: original author of the information.
        :param level: check the hierarchy. If the signed user has a lower value, exception is raised
        :param same: checks if the user that is trying to push changes is the same than the original.
        :return:
        """

        auth_user = User.objects.get(sessionToken=session_token)
        auth_user_rol = auth_user.rol
        original_user = User.objects.get(id=author_id)
        original_user_rol = original_user.rol
        if same and not author_id == auth_user.id:
            raise MessageBasedException(message_id=ErrorMessage.Type.UNAUTHORIZED)
        elif level and auth_user_rol.priority < original_user_rol.priority:
            raise MessageBasedException(message_id=ErrorMessage.Type.UNAUTHORIZED)
