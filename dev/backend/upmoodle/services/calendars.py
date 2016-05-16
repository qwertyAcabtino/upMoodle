from datetime import datetime, timedelta
from sets import Set

import calendar
from upmoodle.models import CalendarDate, Calendar, Level, User
from upmoodle.models.exceptions.messageBasedException import MessageBasedException
from upmoodle.models.message.errorMessage import ErrorMessage

# TODO. Return only related events.
from upmoodle.controllers.decorators.exceptions import map_exceptions
from upmoodle.services.auth import AuthService
from upmoodle.services.level import LevelService


class CalendarService:
    def __init__(self):
        pass

    @staticmethod
    @map_exceptions
    def get_calendar_by_period(period=None, init_date=None):
        if is_valid_init_date_by_period(period, init_date):
            range_date = get_date_range(period, init_date)
            ids = Set()
            events = CalendarDate.objects.filter(date__range=range_date)
            for event in events:
                ids.add(event.calendarId.id)

            return Calendar.objects.filter(id__in=list(ids))

    @staticmethod
    @map_exceptions
    def get_calendar_by_period_user_related(period=None, init_date=None, session_token=None):
        user = User.objects.get(sessionToken=session_token)
        related_ids = LevelService.get_ids_tree_from_childrens(subjects=user.subjects.iterator())
        calendar_events = CalendarService.get_calendar_by_period(period=period, init_date=init_date)
        return calendar_events.filter(level__in=related_ids)

    @staticmethod
    @map_exceptions
    def get_calendar_by_id(calendar_id=None, **kwargs):
        return Calendar.objects.get(id=calendar_id)

    @staticmethod
    @map_exceptions
    def delete_calendar_by_id(session_token=None, calendar_id=None, **kwargs):
        event = Calendar.objects.get(id=calendar_id)
        AuthService.is_authorized_author(session_token=session_token, author_id=event.author_id, level=True)
        event.delete()

    @staticmethod
    @map_exceptions
    def update_calendar_by_id(session_token=None, calendar_id=None, data=None, **kwargs):
        original_calendar = Calendar.objects.get(id=calendar_id)

        AuthService.is_authorized_author(session_token=session_token, author_id=original_calendar.author_id, level=True)
        Level.validate_exists(data)
        fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency']
        calendar_object = Calendar.parse(data, fields=fields, optional=True)
        calendar_object.lastUpdated_id = User.get_signed_user_id(session_token)
        calendar_object.lastUpdate = datetime.now()
        original_calendar.update(calendar_object, fields)
        original_calendar.save()
        return original_calendar

    @staticmethod
    @map_exceptions
    def add_calendar(session_token=None, data=None):
        Level.validate_exists(data)
        fields = ['title', 'text', 'level_id', 'hourStart', 'hourEnd', 'firstDate', 'lastDate', 'allDay', 'frequency_id']
        calendar_object = Calendar.parse(data, fields=fields, optional=True)
        calendar_object.author_id = User.get_signed_user_id(session_token)
        calendar_object.lastUpdated_id = User.get_signed_user_id(session_token)
        AuthService.is_authorized_author(session_token=session_token, author_id=calendar_object.author_id, level=True)
        calendar_object.lastUpdate = datetime.now()
        calendar_object.save()
        return calendar_object


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
            raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)
        else:
            return True
    except ValueError:
        raise MessageBasedException(message_id=ErrorMessage.Type.INCORRECT_DATA)


def get_date_range(period, init_date):
    date_format = '%Y-%m-%d'
    values = init_date.split('-')
    day = int(values[2]) if period == "day" else 1
    date = datetime(int(values[0]), int(values[1]), day)
    start_range = date.strftime(date_format)
    if period == "day":
        return [start_range, start_range]
    else:
        month_days = calendar.monthrange(date.year, date.month)[1] - 1
        end_range = (date + timedelta(month_days)).strftime(date_format)
    return [start_range, end_range]

