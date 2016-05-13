from functools import wraps

from upmoodle.models import ErrorMessage
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from upmoodle.routers.response.jsonfactory import JsonResponseFactory


def map_exceptions(view_func):
    def _decorator(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except (ValidationError, ObjectDoesNotExist, OverflowError, ValueError, KeyError) as v:
            raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA, exception=v)
    return wraps(view_func)(_decorator)


def zero_exceptions(view_func):
    def _decorator(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except (ValidationError, ObjectDoesNotExist, OverflowError, ValueError, KeyError) as v:
            return JsonResponseFactory().error(message_id=ErrorMessage.Type.INCORRECT_DATA, exception=v)
        except MessageBasedException as m:
            return JsonResponseFactory().error(message_id=m.message_id, exception=m).build()
    return wraps(view_func)(_decorator)
