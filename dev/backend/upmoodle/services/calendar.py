from datetime import datetime
from sets import Set

from django.core.exceptions import ObjectDoesNotExist, ValidationError

import calendar
from upmoodle.models import CalendarDate, Calendar, Level, User
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.message.okMessage import OkMessage
from upmoodle.models.utils.jsonResponse import JsonResponse
from upmoodle.models.utils.requestException import RequestException, RequestExceptionByCode, RequestExceptionByMessage
from upmoodle.services.orm.serializers import CalendarEventSerializer

# TODO. Return only related events.
from upmoodle.services.auth import AuthService


class CalendarService:
    def __init__(self):
        pass

    @staticmethod
    def get_calendar_by_period(period=None, init_date=None):
        if is_valid_init_date_by_period(period, init_date):
            range_date = get_date_range(period, init_date)
            ids = Set()
            events = CalendarDate.objects.filter(date__range=range_date)
            for event in events:
                ids.add(event.calendarId.id)

            events = Calendar.objects.filter(id__in=list(ids))
            event_list = CalendarEventSerializer(events, many=True).data
            return JsonResponse(body=event_list)

    @staticmethod
    def get_calendar_by_id(calendar_id=None, **kwargs):
        try:
            event = Calendar.objects.get(id=calendar_id)
            event_dict = CalendarEventSerializer(event, many=False).data
            return JsonResponse(body=event_dict)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def delete_calendar_by_id(session_token=None, calendar_id=None, **kwargs):
        try:
            event = Calendar.objects.get(id=calendar_id)
            AuthService.is_authorized_author(session_token=session_token, author_id=event.author_id, level=True)
            event.delete()
            return JsonResponse(message_id=OkMessage.Type.CALENDAR_EVENT_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def update_calendar_by_id(session_token=None, calendar_id=None, data=None, **kwargs):
        try:
            original_calendar = Calendar.objects.get(id=calendar_id)

            AuthService.is_authorized_author(session_token=session_token, author_id=original_calendar.author_id, level=True)
            Level.validate_exists(data)
            fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency']
            calendar_object = Calendar.parse(data, fields=fields, optional=True)
            calendar_object.lastUpdated_id = User.get_signed_user_id(session_token)
            calendar_object.lastUpdate = datetime.now()
            original_calendar.update(calendar_object, fields)
            original_calendar.save()
            return JsonResponse(message_id=OkMessage.Type.CALENDAR_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def add_calendar(session_token=None, data=None):
        try:
            Level.validate_exists(data)
            fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency_id']
            calendar_object = Calendar.parse(data, fields=fields, optional=True)
            calendar_object.author_id = User.get_signed_user_id(session_token)
            calendar_object.lastUpdated_id = User.get_signed_user_id(session_token)
            AuthService.is_authorized_author(session_token=session_token, author_id=calendar_object.author_id, level=True)
            calendar_object.lastUpdate = datetime.now()
            calendar_object.save()
            return JsonResponse(body=calendar_object, message_id=OkMessage.Type.CALENDAR_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse


def is_valid_month_init_date(init_date):
    values = init_date.split('-')
    return 0 < int(values[1]) < 13 and 2010 < int(values[0]) < 2100


def is_valid_day_init_date(init_date):
    try:
        datetime.datetime.strptime(init_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_init_date_by_period(period, init_date):
    try:
        valid_date = True
        if period == "month":
            valid_date = is_valid_month_init_date(init_date)
        elif period == "day":
            valid_date = is_valid_day_init_date(init_date)
        if not valid_date:
            raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
        else:
            return True
    except ValueError:
        raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)


def get_date_range(period, init_date):
    date_format = '%Y-%m-%d'
    values = init_date.split('-')
    day = int(values[2]) if period == "day" else 1
    date = datetime.datetime(int(values[0]), int(values[1]), day)
    start_range = date.strftime(date_format)
    if period == "day":
        return [start_range, start_range]
    else:
        month_days = calendar.monthrange(date.year, date.month)[1] - 1
        end_range = (date + datetime.timedelta(month_days)).strftime(date_format)
    return [start_range, end_range]

