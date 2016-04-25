from django.views.decorators.csrf import csrf_exempt

from rest.controllers.requests import check_cookies, method, authenticated
from rest.services.auth import AuthService


@csrf_exempt
@method('POST')
def login(request):
    return AuthService.login(request)


@csrf_exempt
@method('POST')
def signup(request):
    return AuthService.signup(request)


@csrf_exempt
@authenticated
@method('POST')
def logout(request):
    return AuthService.logout(request)


@csrf_exempt
@method('POST')
def confirm_email(request):
    return AuthService.confirm_email(request)


@csrf_exempt
@method('POST')
def recover_password(request):
    return AuthService.recover_password(request)
