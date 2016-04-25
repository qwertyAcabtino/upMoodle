from datetime import datetime
from sets import Set

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import is_valid_initDate_by_period, get_date_range, \
    is_authorized_author
from rest.models import CalendarDate, Calendar, Level, User
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.serializers import CalendarEventSerializer

# TODO. Return only related events.
from rest.orm.unserializer import unserialize_calendar


class CalendarService:
    def __init__(self):
        pass

    @staticmethod
    def get_calendar_by_period(period=None, init_date=None):
        if is_valid_initDate_by_period(period, init_date):
            range_date = get_date_range(period, init_date)
            ids = Set()
            events = CalendarDate.objects.filter(date__range=range_date)
            for event in events:
                ids.add(event.calendarId.id)

            events = Calendar.objects.filter(id__in=list(ids))
            serializer = CalendarEventSerializer(events, many=True)
            return JSONResponse(serializer.data)

    @staticmethod
    def get_calendar_by_id(calendar_id=None, **kwargs):
        try:
            event = Calendar.objects.get(id=calendar_id)
            serializer = CalendarEventSerializer(event, many=False)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def delete_calendar_by_id(session_token=None, calendar_id=None, **kwargs):
        try:
            event = Calendar.objects.get(id=calendar_id)
            is_authorized_author(session_token=session_token, author_id=event.author_id, level=True)
            event.delete()
            return JSONResponseID(MessageType.CEVENT_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def update_calendar_by_id(session_token=None, calendar_id=None, data=None, **kwargs):
        try:
            original_calendar = Calendar.objects.get(id=calendar_id)

            is_authorized_author(session_token=session_token, author_id=original_calendar.author_id, level=True)
            Level.validate_exists(data)
            fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency']
            calendar = unserialize_calendar(data, fields=fields, optional=True)
            calendar.lastUpdated_id = User.get_signed_user_id(session_token)
            calendar.lastUpdate = datetime.now()
            original_calendar.update(calendar, fields)
            original_calendar.save()
            return JSONResponseID(MessageType.CALENDAR_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def add_calendar(session_token=None, data=None):
        try:
            Level.validate_exists(data)
            fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency_id']
            calendar = unserialize_calendar(data, fields=fields, optional=True)
            calendar.author_id = User.get_signed_user_id(session_token)
            calendar.lastUpdated_id = User.get_signed_user_id(session_token)
            is_authorized_author(session_token=session_token, author_id=calendar.author_id, level=True)
            calendar.lastUpdate = datetime.now()
            calendar.save()
            return JSONResponse({"calendarId": calendar.id}, status=200)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse



