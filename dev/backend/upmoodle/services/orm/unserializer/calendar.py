# from upmoodle.models import Calendar
# from upmoodle.models.message.errorMessage import ErrorMessage
# from upmoodle.models.utils.requestException import RequestExceptionByCode
# from upmoodle.services.orm.unserializer import unserialize
#
#
# def unserialize_calendar(form, *args, **kwargs):
#     fields = kwargs.get('fields', None)
#     optional = kwargs.get('optional', False)
#     if fields:
#         calendar = Calendar()
#         return unserialize(calendar, fields, form, optional=optional)
#     else:
#         raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
