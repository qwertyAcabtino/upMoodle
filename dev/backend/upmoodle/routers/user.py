from django.views.decorators.csrf import csrf_exempt

from upmoodle.routers.decorators.routing_decorators import authenticated, methods, method, response
from upmoodle.services.user import UserService


@csrf_exempt
@authenticated
@methods(('GET', 'POST', 'DELETE'))
@response(media_type='application/json')
def user_endpoint(request, session_token=None, data=None):

    # @response(media_type='application/json')
    # def get_me(session_token=None, data=None):
    #     return UserService.get_me(session_token=session_token, data=data)
    #
    # @response(media_type='application/json')
    # def update_me(session_token=None, data=None):
    #     return UserService.update_me(session_token=session_token, data=data)
    #
    # @response(media_type='application/json')
    # def delete_me(session_token=None, data=None):
    #     return UserService.delete_me(session_token=session_token, data=data)

    service_methods = {
        'GET': UserService.get_me,
        'DELETE': UserService.delete_me,
        'POST': UserService.update_me,
    }

    return service_methods[request.method](session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
@response(media_type='application/json')
def user_subjects(request, session_token=None, data=None):
    return UserService.update_me_subjects(session_token=session_token, data=data)


@csrf_exempt
@authenticated
@method('POST')
@response(media_type='application/json')
def user_avatar(request, session_token=None, **kwargs):
    files = request.FILES
    return UserService.update_me_avatar(session_token=session_token, files=files)


@authenticated
@method('GET')
@response(media_type='application/json')
def user_by_id(request, pk, **kwargs):
    return UserService.get_user_by_id(user_id=pk)


@authenticated
@method('GET')
@response(media_type='application/json')
def users_by_rol(request, pk, **kwargs):
    return UserService.get_users_by_rol(rol_id=pk)
