import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from backend import settings
from backend.settings import SESSION_COOKIE_NAME
from rest.JSONResponse import JSONResponseID, JSONResponse
from rest.controllers.Exceptions.requestException import RequestExceptionByCode, RequestException, \
    RequestExceptionByMessage
from rest.controllers.controllers import cookies_are_ok, check_cookies, get_email_confirmation_message, \
    check_request_method, get_random_password, send_recover_password_email
from rest.models import User
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.unserializer import unserialize_user


class AuthService:

    def __init__(self):
        pass

    @staticmethod
    def get_cookie(request):
        if not cookies_are_ok(request):
            return uuid.uuid4().hex
        else:
            return request.COOKIES[SESSION_COOKIE_NAME]

    @staticmethod
    def login(request):
        try:
            session_token = AuthService.get_cookie(request)

            request_email = request.POST['email']
            request_pass = request.POST['password']
            user = User.objects.get(email=request_email, password=request_pass)
            if not user.confirmedEmail:
                return RequestExceptionByCode(ErrorMessageType.UNCONFIRMED_EMAIL).jsonResponse
            else:
                user.sessionToken = session_token
                user.lastTimeActive = timezone.now()
                user.save()
                json_response = JSONResponseID(MessageType.SUCCESS_LOGIN)
                json_response.set_cookie(settings.SESSION_COOKIE_NAME, session_token)
                return json_response
        except ObjectDoesNotExist or MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except RequestException as r:
            return r.jsonResponse

    @staticmethod
    def signup(request):
        try:
            session_token = AuthService.get_cookie(request)

            user = unserialize_user(request.POST, sessionToken=session_token,
                                    fields=['email', 'password', 'nick', 'name'])
            send_mail('Email confirmation',
                      get_email_confirmation_message(request, cookie=session_token),
                      'info@upmoodle.com', [user.email],
                      fail_silently=False)
            user.save()
            json_response = JSONResponse({"userId": user.id}, status=200)
            json_response.set_cookie(settings.SESSION_COOKIE_NAME, session_token)
            return json_response
        except ValidationError as v:
            r = RequestExceptionByMessage(v)
            return r.jsonResponse
        except RequestException as r:
            return r.jsonResponse
        except Exception:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def logout(request):
        try:
            session_token = AuthService.get_cookie(request)
            user = User.objects.get(sessionToken=session_token)
            user.sessionToken = ''
            user.save()
            json_response = JSONResponse({"null"}, status=200)
            json_response.delete_cookie(SESSION_COOKIE_NAME)
            return json_response
        except Exception:
            return JSONResponse({"null"}, status=400)

    @staticmethod
    def confirm_email(request):
        try:
            token = request.POST['token']
            user = User.objects.get(sessionToken=token)
            if user.confirmedEmail:
                return RequestExceptionByCode(ErrorMessageType.ALREADY_CONFIRMED).jsonResponse
            else:
                user.confirmedEmail = True
                user.save()
                return JSONResponseID(MessageType.ACCOUNT_VALIDATED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def recover_password(request):
        try:
            email_request = request.POST['email']
            user = User.objects.get(email=email_request)
            if not user.confirmedEmail:
                raise RequestExceptionByCode(ErrorMessageType.UNCONFIRMED_EMAIL)
            elif user.banned:
                raise RequestExceptionByCode(ErrorMessageType.UNAUTHORIZED)
            else:
                password = get_random_password()
                send_recover_password_email(user.email, password)
                user.password = password
                user.save()
            return JSONResponseID(MessageType.RECOVER_PASS_EMAIL)
        except RequestException as r:
            return r.jsonResponse
        except Exception:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

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
