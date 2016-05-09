import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.utils import timezone

from backend import settings
from backend.settings import SESSION_COOKIE_NAME
from rest.models import User
from rest.models.message.errorMessage import ErrorMessage
from rest.models.message.okMessage import OkMessage
from rest.models.utils.jsonResponse import JsonResponse
from rest.models.utils.requestException import RequestExceptionByCode, RequestException, \
    RequestExceptionByMessage
from rest.services.orm.unserializer import unserialize_user
from rest.services.utils.email import EmailService
from rest.services.utils.password import PasswordService


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
    def login(session_token=None, data=None):
        try:
            session_token = AuthService.get_cookie(session_token)

            request_email = data['email']
            request_pass = data['password']
            user = User.objects.get(email=request_email, password=request_pass)
            if not user.confirmedEmail:
                return RequestExceptionByCode(ErrorMessage.Type.UNCONFIRMED_EMAIL).jsonResponse
            else:
                user.sessionToken = session_token
                user.lastTimeActive = timezone.now()
                user.save()
                json_response = JsonResponse(message_id=OkMessage.Type.SUCCESS_LOGIN)
                json_response.set_cookie(settings.SESSION_COOKIE_NAME, session_token)
                return json_response
        except (ObjectDoesNotExist, KeyError):
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except RequestException as r:
            return r.jsonResponse

    @staticmethod
    def signup(request, session_token=None, data=None):
        try:
            session_token = AuthService.get_cookie(session_token)

            user = unserialize_user(data, sessionToken=session_token,
                                    fields=['email', 'password', 'nick', 'name'])
            send_mail('Email confirmation',
                      EmailService.get_email_confirmation_message(request, cookie=session_token),
                      'info@upmoodle.com', [user.email],
                      fail_silently=False)
            user.save()
            json_response = JsonResponse(body=user)
            json_response.set_cookie(settings.SESSION_COOKIE_NAME, session_token)
            return json_response
        except ValidationError as v:
            r = RequestExceptionByMessage(v)
            return r.jsonResponse
        except RequestException as r:
            return r.jsonResponse
        except Exception:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def logout(session_token=None):
        try:
            session_token = AuthService.get_cookie(session_token)
            user = User.objects.get(sessionToken=session_token)
            user.sessionToken = ''
            user.save()
            json_response = JsonResponse(message_id=OkMessage.Type.SUCCESS_LOGOUT)
            json_response.set_cookie(SESSION_COOKIE_NAME, '')
            return json_response
        except Exception:
            return JsonResponse(message_id=OkMessage.Type.SUCCESS_LOGOUT)

    @staticmethod
    def confirm_email(session_token=None):
        try:
            user = User.objects.get(sessionToken=session_token)
            if user.confirmedEmail:
                return RequestExceptionByCode(ErrorMessage.Type.ALREADY_CONFIRMED).jsonResponse
            else:
                user.confirmedEmail = True
                user.save()
                return JsonResponse(message_id=OkMessage.Type.ACCOUNT_VALIDATED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def recover_password(data=None):

        try:
            email_request = data['email']
            user = User.objects.get(email=email_request)
            if not user.confirmedEmail:
                raise RequestExceptionByCode(ErrorMessage.Type.UNCONFIRMED_EMAIL)
            elif user.banned:
                raise RequestExceptionByCode(ErrorMessage.Type.UNAUTHORIZED)
            else:
                password = PasswordService.get_random()
                EmailService.send_recover_password_email(user.email, password)
                user.password = password
                user.save()
                return JsonResponse(message_id=OkMessage.Type.RECOVER_PASS_EMAIL)
        except RequestException as r:
            return r.jsonResponse
        except Exception:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

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
            raise RequestExceptionByCode(ErrorMessage.Type.UNAUTHORIZED)
        elif level and auth_user_rol.priority < original_user_rol.priority:
            raise RequestExceptionByCode(ErrorMessage.Type.UNAUTHORIZED)
