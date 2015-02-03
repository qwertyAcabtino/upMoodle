import datetime
from rest.JSONResponse import JSONResponse
from rest.controllers.controllers import check_signed_in_request, is_valid_initDate_by_period
from rest.models import Calendar


def calendar_get_by_period(request, period, initDate):
    check_signed_in_request(request, method='GET')
    if is_valid_initDate_by_period(period, initDate):
        # range = get_date_range
        events = Calendar.objects.filter(firstDate__range=["2015-02-01", "2015-02-01"])
        return JSONResponse({"noteId": "1"}, status=200)
        # Match events for desired date.
        # Return (frontend does the rest).
