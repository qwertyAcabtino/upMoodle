from django.views.decorators.csrf import csrf_exempt

from upmoodle.models import OkMessage
from upmoodle.routers.decorators.routing_decorators import method, authenticated
from upmoodle.routers.decorators.zero_exception_decorator import zero_exceptions
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.auth import AuthService


@csrf_exempt
@method('POST')
@zero_exceptions
def login(request, session_token=None, data=None):
    cookies = AuthService.login(session_token=session_token, data=data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.SUCCESS_LOGIN).cookies(cookies=cookies).build()


@csrf_exempt
@method('POST')
@zero_exceptions
def signup(request, session_token=None, data=None):
    cookies = AuthService.signup(session_token=session_token, data=data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.SUCCESS_SIGNUP).cookies(cookies=cookies).build()


@csrf_exempt
@authenticated
@method('POST')
@zero_exceptions
def logout(request, session_token=None, **kwargs):
    cookies = AuthService.logout(session_token=session_token)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.SUCCESS_LOGOUT).cookies(cookies=cookies).build()


@csrf_exempt
@method('POST')
@zero_exceptions
def confirm_email(request, data=None, **kwargs):
    AuthService.confirm_email(session_token=data['token'])
    return JsonResponseFactory().ok(message_id=OkMessage.Type.ACCOUNT_VALIDATED).build()


@csrf_exempt
@method('POST')
@zero_exceptions
def recover_password(request, data=None, **kwargs):
    AuthService.recover_password(data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.RECOVER_PASS_EMAIL).build()
