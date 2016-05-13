from django.views.decorators.csrf import csrf_exempt

from upmoodle.routers.decorators.routing_decorators import method, authenticated
from upmoodle.routers.decorators.zero_exception_decorator import zero_exceptions
from upmoodle.services.auth import AuthService


@csrf_exempt
@method('POST')
@zero_exceptions
def login(request, session_token=None, data=None):
    return AuthService.login(session_token=session_token, data=data)

@csrf_exempt
@method('POST')
def signup(request, session_token=None, data=None):
    return AuthService.signup(session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
def logout(request, session_token=None, **kwargs):
    return AuthService.logout(session_token=session_token)


@csrf_exempt
@method('POST')
def confirm_email(request, data=None, **kwargs):
    session_token = data['token']
    return AuthService.confirm_email(session_token=session_token)


@csrf_exempt
@method('POST')
def recover_password(request, data=None, **kwargs):
    return AuthService.recover_password(data)
