from django.views.decorators.csrf import csrf_exempt

from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, methods, method
from upmoodle.models import OkMessage
from upmoodle.routers.response.factory import ResponseFactory
from upmoodle.services.notes import NoteService
from upmoodle.services.user import UserService


@zero_exceptions
@csrf_exempt
@authenticated
@methods(('GET', 'POST', 'DELETE'))
def user_endpoint(request, session_token=None, data=None):

    def get_me(session_token=None, data=None):
        user = UserService.get_me(session_token=session_token, data=data)
        return ResponseFactory().ok().body(obj=user).build()

    def update_me(session_token=None, data=None):
        UserService.update_me(session_token=session_token, data=data)
        return ResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()

    def delete_me(session_token=None, data=None):
        UserService.delete_me(session_token=session_token, data=data)
        return ResponseFactory().ok(message_id=OkMessage.Type.USER_REMOVED).build()

    service_methods = {
        'GET': get_me,
        'DELETE': delete_me,
        'POST': update_me,
    }

    return service_methods[request.method](session_token=session_token, data=data)


@zero_exceptions
@csrf_exempt
@authenticated
@method('POST')
def user_subjects(request, session_token=None, data=None):
    UserService.update_me_subjects(session_token=session_token, data=data)
    return ResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()


@zero_exceptions
@csrf_exempt
@authenticated
@method('POST')
def user_avatar(request, session_token=None, **kwargs):
    files = request.FILES
    UserService.update_me_avatar(session_token=session_token, files=files)
    return ResponseFactory().ok(message_id=OkMessage.Type.USER_UPDATED).build()


@zero_exceptions
@authenticated
@method('GET')
def user_by_id(request, pk, **kwargs):
    user = UserService.get_user_by_id(user_id=pk)
    return ResponseFactory().ok().body(obj=user).build()


@zero_exceptions
@authenticated
@method('GET')
def users_by_rol(request, pk, **kwargs):
    users = UserService.get_users_by_rol(rol_id=pk)
    return ResponseFactory().ok().body(obj=users).build()


