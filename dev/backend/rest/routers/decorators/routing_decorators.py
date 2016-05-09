import json
import uuid
from functools import wraps

import demjson as demjson

from backend.settings import SESSION_COOKIE_NAME
from rest.exceptions.requestException import RequestExceptionByCode
from rest.models.message.errorMessage import ErrorMessage
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


def method(method_value):
    def _method_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            if not request.method == method_value:
                return RequestExceptionByCode(ErrorMessage.Type.NOT_ALLOWED_METHOD).jsonResponse
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
                return RequestExceptionByCode(ErrorMessage.Type.NOT_ALLOWED_METHOD).jsonResponse
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
        exception = RequestExceptionByCode(ErrorMessage.Type.DISABLED_COOKIES)
        exception.jsonResponse.set_cookie(SESSION_COOKIE_NAME, uuid.uuid4().hex)
        raise exception


def _check_signed_in(request):
    _check_cookies(request)
    if not AuthService.is_authenticated(request.COOKIES[SESSION_COOKIE_NAME]):
        raise RequestExceptionByCode(ErrorMessage.Type.NOT_SIGNED_IN)


def _body_to_json(body):
    try:
        return demjson.decode(body)
    except:
        return dict()