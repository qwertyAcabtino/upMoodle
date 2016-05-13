from django.views.decorators.csrf import csrf_exempt

from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, methods, method
from upmoodle.models import OkMessage
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.calendar import CalendarService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
@zero_exceptions
def calendar_by_id(request, calendar_id, session_token=None, data=None):

    def delete(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs):
        CalendarService.delete_calendar_by_id(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.CALENDAR_EVENT_REMOVED).build()

    def update(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs):
        calendar = CalendarService.update_calendar_by_id(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs)
        return JsonResponseFactory().ok(message_id=OkMessage.Type.CALENDAR_UPDATED).identity(calendar).build()

    def get(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs):
        calendar_in = CalendarService.get_calendar_by_id(session_token=session_token, calendar_id=calendar_id, data=data, **kwargs)
        return JsonResponseFactory().ok().body(obj=calendar_in).build()

    service_methods = {
        'GET': get,
        'PUT': update,
        'DELETE': delete,
    }
    return service_methods[request.method](session_token=session_token, data=data, calendar_id=calendar_id)


@csrf_exempt
@authenticated
@method('GET')
@zero_exceptions
def calendar_by_period(request, period, init_date, **kwargs):
    calendar_in = CalendarService.get_calendar_by_period(period, init_date)
    return JsonResponseFactory().ok().body(obj=calendar_in).build()


@csrf_exempt
@authenticated
@method('POST')
@zero_exceptions
def calendar_endpoint(request, session_token=None, data=None):
    calendar = CalendarService.add_calendar(session_token=session_token, data=data)
    return JsonResponseFactory().ok(message_id=OkMessage.Type.CALENDAR_UPDATED).identity(calendar).build()
