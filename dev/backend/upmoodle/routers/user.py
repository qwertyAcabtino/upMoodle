from django.views.decorators.csrf import csrf_exempt

from upmoodle.models import OkMessage
from upmoodle.routers.decorators.routing_decorators import authenticated, methods, method
from upmoodle.routers.decorators.zero_exception_decorator import zero_exceptions
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.user import UserService


@csrf_exempt
@authenticated
@methods(('GET', 'POST', 'DELETE'))
@zero_exceptions
def user_endpoint(request, session_token=None, data=None):

    def get_me(session_token=None, data=None):
        user = UserService.get_me(session_token=session_token, data=data)
        return JsonResponseFactory().ok().body(obj=user).build()

    def update_me(session_token=None, data=None):
        UserService.update_me(session_token=session_token, data=data)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()

    def delete_me(session_token=None, data=None):
        UserService.delete_me(session_token=session_token, data=data)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.USER_REMOVED).build()

    service_methods = {
        'GET': get_me,
        'DELETE': delete_me,
        'POST': update_me,
    }

    return service_methods[request.method](session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
@zero_exceptions
def user_subjects(request, session_token=None, data=None):
    UserService.update_me_subjects(session_token=session_token, data=data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()


@csrf_exempt
@authenticated
@method('POST')
@zero_exceptions
def user_avatar(request, session_token=None, **kwargs):
    files = request.FILES
    UserService.update_me_avatar(session_token=session_token, files=files)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()


@authenticated
@method('GET')
@zero_exceptions
def user_by_id(request, pk, **kwargs):
    user = UserService.get_user_by_id(user_id=pk)
    return JsonResponseFactory().ok().body(obj=user).build()


@authenticated
@method('GET')
@zero_exceptions
def users_by_rol(request, pk, **kwargs):
    users = UserService.get_user_by_id(user_id=pk)
    return JsonResponseFactory().ok().body(obj=users).build()
