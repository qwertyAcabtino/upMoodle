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
