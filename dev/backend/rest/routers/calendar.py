from django.views.decorators.csrf import csrf_exempt

from rest.routers.decorators.routing_decorators import authenticated, methods, method
from rest.services.calendar import CalendarService


@csrf_exempt
@authenticated
@methods(('GET', 'PUT', 'DELETE'))
def calendar_by_id(request, calendar_id, session_token=None, data=None):
    service_methods = {
        'GET': CalendarService.get_calendar_by_id,
        'PUT': CalendarService.update_calendar_by_id,
        'DELETE': CalendarService.delete_calendar_by_id,
    }
    return service_methods[request.method](session_token=session_token, data=data, calendar_id=calendar_id)


@csrf_exempt
@authenticated
@method('GET')
def calendar_by_period(request, period, init_date, **kwargs):
    return CalendarService.get_calendar_by_period(period, init_date)


@csrf_exempt
@authenticated
@method('POST')
def calendar_endpoint(request, session_token=None, data=None):
    return CalendarService.add_calendar(session_token=session_token, data=data)
