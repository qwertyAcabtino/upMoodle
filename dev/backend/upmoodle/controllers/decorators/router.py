import uuid
from functools import wraps

import demjson as demjson

from backend.settings import SESSION_COOKIE_NAME
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.auth import AuthService


def authenticated(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            _check_signed_in(request)
        except MessageBasedException as m:
            return JsonResponseFactory().error(message_id=m.message_id, exception=m).build()

        kwargs['session_token'] = request.COOKIES[SESSION_COOKIE_NAME]
        response = view_func(request, *args, **kwargs)
        response = _ensure_cookie(response, kwargs['session_token'])
        return response
    return wraps(view_func)(_decorator)


def method(method_value):
    def _method_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            if not request.method == method_value:
                raise MessageBasedException(message_id=ErrorMessage.Type.NOT_ALLOWED_METHOD)
            else:
                if method_value == 'POST':
                    kwargs['data'] = _body_to_json(request.body)
                    if request.POST:
                        kwargs['data'].update(request.POST.dict())
                elif method_value == 'GET':
                    kwargs['data'] = request.GET
                elif method_value == 'PUT':
                    kwargs['data'] = _body_to_json(request.body)

                response = view_func(request, *args, **kwargs)
                return response

        return wraps(view_func)(_decorator)
    return _method_decorator


def methods(methods_list):
    def _method_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            if request.method not in methods_list:
                raise MessageBasedException(message_id=ErrorMessage.Type.NOT_ALLOWED_METHOD)
            else:

                if 'POST' in methods_list and request.method == 'POST':
                    kwargs['data'] = _body_to_json(request.body)
                elif 'PUT' in methods_list and request.method == 'PUT':
                    kwargs['data'] = _body_to_json(request.body)
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
        return JsonResponseFactory().error(message_id=ErrorMessage.Type.DISABLED_COOKIES).cookies(cookies={SESSION_COOKIE_NAME: uuid.uuid4().hex}).build()


def _check_signed_in(request):
    _check_cookies(request)
    if not AuthService.is_authenticated(request.COOKIES[SESSION_COOKIE_NAME]):
        raise MessageBasedException(message_id=ErrorMessage.Type.NOT_SIGNED_IN)


def _body_to_json(body):
    try:
        return demjson.decode(body)
    except:
        return dict()
