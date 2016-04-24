from django.views.decorators.csrf import csrf_exempt

from rest.services.auth import AuthService


@csrf_exempt
def login(request):
    return AuthService.login(request)


@csrf_exempt
def signup(request):
    return AuthService.signup(request)


@csrf_exempt
def logout(request):
    return AuthService.logout(request)


@csrf_exempt
def confirm_email(request):
    return AuthService.confirm_email(request)


@csrf_exempt
def recover_password(request):
    return AuthService.recover_password(request)
