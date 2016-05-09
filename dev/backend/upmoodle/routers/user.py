from django.views.decorators.csrf import csrf_exempt

from upmoodle.routers.decorators.routing_decorators import authenticated, methods, method
from upmoodle.services.user import UserService


@csrf_exempt
@authenticated
@methods(('GET', 'POST', 'DELETE'))
def user_endpoint(request, session_token=None, data=None):
    service_methods = {
        'GET': UserService.get_me,
        'DELETE': UserService.delete_me,
        'POST': UserService.update_me,
    }
    return service_methods[request.method](session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
def user_subjects(request, session_token=None, data=None):
    service_methods = {
        'POST': UserService.update_me_subjects,
    }
    return service_methods[request.method](session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
def user_avatar(request, session_token=None, **kwargs):
    files = request.FILES
    return UserService.update_me_avatar(session_token=session_token, files=files)


@authenticated
@method('GET')
def user_by_id(request, pk, **kwargs):
    return UserService.get_user_by_id(user_id=pk)


@authenticated
@method('GET')
def users_by_rol(request, pk, **kwargs):
    return UserService.get_users_by_rol(rol_id=pk)
