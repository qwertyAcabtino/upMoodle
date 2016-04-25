import uuid
from functools import wraps

from backend.settings import SESSION_COOKIE_NAME
from rest.controllers.Exceptions.requestException import RequestExceptionByCode
from rest.controllers.controllers import cookies_are_ok, is_signed_in
from rest.models.message.errorMessage import ErrorMessageType


def authenticated(view_func):
    def _decorator(request, *args, **kwargs):
        try:
            _check_cookies(request)
            _check_signed_in(request)
        except RequestExceptionByCode as r:
            return r.jsonResponse

        response = view_func(request, *args, **kwargs)
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
                return RequestExceptionByCode(ErrorMessageType.NOT_ALLOWED_METHOD).jsonResponse
            else:
                response = view_func(request, *args, **kwargs)
                return response

        return wraps(view_func)(_decorator)
    return _method_decorator


def _check_cookies(request):
    if not cookies_are_ok(request):
        exception = RequestExceptionByCode(ErrorMessageType.DISABLED_COOKIES)
        exception.jsonResponse.set_cookie(SESSION_COOKIE_NAME, uuid.uuid4().hex)
        raise exception


def _check_signed_in(request):
    if not is_signed_in(request):
        raise RequestExceptionByCode(ErrorMessageType.NOT_SIGNED_IN)
