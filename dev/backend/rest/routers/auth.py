from django.views.decorators.csrf import csrf_exempt

from rest.controllers.requests import check_cookies, method, authenticated
from rest.services.auth import AuthService


@csrf_exempt
@method('POST')
def login(request, **kwargs):
    return AuthService.login(request)


@csrf_exempt
@method('POST')
def signup(request, **kwargs):
    return AuthService.signup(request)


@csrf_exempt
@authenticated
@method('POST')
def logout(request, **kwargs):
    return AuthService.logout(request)


@csrf_exempt
@method('POST')
def confirm_email(request, **kwargs):
    return AuthService.confirm_email(request)


@csrf_exempt
@method('POST')
def recover_password(request, **kwargs):
    return AuthService.recover_password(request)
