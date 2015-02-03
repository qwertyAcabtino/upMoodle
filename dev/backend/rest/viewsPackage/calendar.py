from rest.JSONResponse import JSONResponse
from rest.controllers.controllers import check_signed_in_request, is_valid_initDate_by_period, get_date_range
from rest.models import CalendarDate

# TODO. Check if validators return message.
def calendar_get_by_period(request, period, initDate):
    check_signed_in_request(request, method='GET')
    if is_valid_initDate_by_period(period, initDate):
        rangeDate = get_date_range(period, initDate)
        events = CalendarDate.objects.filter(date__range=rangeDate)
        return JSONResponse({"noteId": "1"}, status=200)
        # Match events for desired date.
        # Return (frontend does the rest).


