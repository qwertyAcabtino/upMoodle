import uuid
from functools import wraps

import demjson as demjson

from backend.settings import SESSION_COOKIE_NAME
from rest.exceptions.requestException import RequestExceptionByCode
from rest.models.message.errorMessage import ErrorMessageType
from rest.services.auth import AuthService


def authenticated(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            _check_signed_in(request)
        except RequestExceptionByCode as r:
            return r.jsonResponse

        kwargs['session_token'] = request.COOKIES[SESSION_COOKIE_NAME]
        response = view_func(request, *args, **kwargs)
        response = _ensure_cookie(response, kwargs['session_token'])
        return response
    return wraps(view_func)(_decorator)


def check_cookies(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            _check_cookies(request)
        except RequestExceptionByCode as r:
            return r.jsonResponse

        response = view_func(request, *args, **kwargs)
        return response

    return wraps(view_func)(_decorator)


# def authorized(same=True, level=False):
#     def _authorized_decorator(view_func):
#         def _decorator(request, *args, **kwargs):
#             """
#             :param request: here comes the information for the signed user.
#             :param author_id: original author of the information.
#             :param level: check the hierarchy. If the signed user has a lower value, exception is raised
#             :param same: checks if the user that is trying to push changes is the same than the original.
#             :return:
#             """
#
#             auth_user = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME])
#             auth_user_rol = auth_user.rol
#             original_user = User.objects.get(id=author_id)
#             original_user_rol = original_user.rol
#             if same and not author_id == userSigned.id:
#                 raise RequestExceptionByCode(ErrorMessageType.UNAUTHORIZED)
#             elif level and rolSigned.priority < rolAuthor.priority:
#                 raise RequestExceptionByCode(ErrorMessageType.UNAUTHORIZED)
#             else:
#                 response = view_func(request, *args, **kwargs)
#                 return response
#
#         return wraps(view_func)(_decorator)
#     return _authorized_decorator()


def method(method_value):
    def _method_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            if not request.method == method_value:
                return RequestExceptionByCode(ErrorMessageType.NOT_ALLOWED_METHOD).jsonResponse
            else:
                if method_value == 'POST':
                    kwargs['data'] = demjson.decode(request.body)
                elif method_value == 'GET':
                    kwargs['data'] = request.GET
                elif method_value == 'PUT':
                    kwargs['data'] = demjson.decode(request.body)

                response = view_func(request, *args, **kwargs)
                return response

        return wraps(view_func)(_decorator)
    return _method_decorator


def methods(methods_list):
    def _method_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            if not request.method in methods_list:
                return RequestExceptionByCode(ErrorMessageType.NOT_ALLOWED_METHOD).jsonResponse
            else:

                if 'POST' in methods_list and request.method == 'POST':
                    kwargs['data'] = demjson.decode(request.body)
                elif 'PUT' in methods_list and request.method == 'PUT':
                    kwargs['data'] = demjson.decode(request.body)
                elif 'PUT' in methods_list and request.method == 'GET':
                    kwargs['data'] = request.GET

                response = view_func(request, *args, **kwargs)
                return response

        return wraps(view_func)(_decorator)
    return _method_decorator


def _ensure_cookie(response, session_token):
    if len(response.cookies) > 0 and response.cookies[SESSION_COOKIE_NAME] and response.cookies[SESSION_COOKIE_NAME].value == '':
        response.set_cookie(SESSION_COOKIE_NAME, session_token)
    return response


def _check_cookies(request):

    def cookies_are_ok():
        return len(request.COOKIES) != 0 and request.COOKIES[SESSION_COOKIE_NAME] and not len(request.COOKIES[SESSION_COOKIE_NAME]) == 0

    if not cookies_are_ok():
        exception = RequestExceptionByCode(ErrorMessageType.DISABLED_COOKIES)
        exception.jsonResponse.set_cookie(SESSION_COOKIE_NAME, uuid.uuid4().hex)
        raise exception


def _check_signed_in(request):
    _check_cookies(request)
    if not AuthService.is_authenticated(request.COOKIES[SESSION_COOKIE_NAME]):
        raise RequestExceptionByCode(ErrorMessageType.NOT_SIGNED_IN)
