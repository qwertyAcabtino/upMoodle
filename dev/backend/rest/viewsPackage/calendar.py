from datetime import datetime
from sets import Set

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt

from backend.settings import SESSION_COOKIE_NAME
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.MESSAGES_ID import INCORRECT_DATA, CEVENT_REMOVED, CALENDAR_UPDATED
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, is_valid_initDate_by_period, get_date_range, \
    check_authorized_author
from rest.models import CalendarDate, Calendar, Level, User
from rest.orm.serializers import CalendarEventSerializer

# TODO. Return only related events.
from rest.orm.unserializers import unserialize_calendar


def calendar_get_by_period(request, period, initDate):
    check_signed_in_request(request, method='GET')
    if is_valid_initDate_by_period(period, initDate):
        rangeDate = get_date_range(period, initDate)
        ids = Set()
        events = CalendarDate.objects.filter(date__range=rangeDate)
        for event in events:
            ids.add(event.calendarId.id)

        events = Calendar.objects.filter(id__in=list(ids))
        serializer = CalendarEventSerializer(events, many=True)
        return JSONResponse(serializer.data)


def calendar_get(request, pk):
    try:
        check_signed_in_request(request, method='GET')
        event = Calendar.objects.get(id=pk)
        serializer = CalendarEventSerializer(event, many=False)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def calendar_delete(request, pk):
    try:
        check_signed_in_request(request, method='DELETE')
        event = Calendar.objects.get(id=pk)
        check_authorized_author(request, event.author_id, level=True)
        event.delete()
        return JSONResponseID(CEVENT_REMOVED)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


def calendar_put(request, pk):
    try:
        calendarOriginal = Calendar.objects.get(id=pk)

        check_authorized_author(request, calendarOriginal.author_id, level=True)
        check_signed_in_request(request, method='POST')
        form = request.POST
        Level.validate_exists(form)
        fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency']
        calendar = unserialize_calendar(form, fields=fields, optional=True)
        calendar.lastUpdated_id = User.get_signed_user_id(request.COOKIES[SESSION_COOKIE_NAME])
        calendar.lastUpdate = datetime.now()
        calendarOriginal.update(calendar, fields)
        calendarOriginal.save()
        return JSONResponseID(CALENDAR_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse


def calendar_post(request):
    try:
        check_signed_in_request(request, method='POST')

        form = request.POST
        Level.validate_exists(form)
        fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency_id']
        calendar = unserialize_calendar(form, fields=fields, optional=True)
        calendar.author_id = User.get_signed_user_id(request.COOKIES[SESSION_COOKIE_NAME])
        calendar.lastUpdated_id = User.get_signed_user_id(request.COOKIES[SESSION_COOKIE_NAME])
        check_authorized_author(request, calendar.author_id, level=True)
        calendar.lastUpdate = datetime.now()
        calendar.save()
        return JSONResponse({"calendarId": calendar.id}, status=200)
    except RequestException as r:
        return r.jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse



