import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Year(models.Model):
    id = models.AutoField(primary_key=True)
    verbose = models.CharField(max_length=20)

    def __unicode__(self):
        return self.verbose

    @staticmethod
    def get_actual_year():
        now = datetime.datetime.now()
        if now.month >= 9:
            verbose = "%s/%s" % (now.year, (now.year + 1),)
        else:
            verbose = "%s/%s" % ((now.year - 1), now.year,)
        try:
            return Year.objects.get(verbose=verbose)
        except ObjectDoesNotExist:
            newYear = Year(verbose=verbose)
            newYear.save()
            return newYear

