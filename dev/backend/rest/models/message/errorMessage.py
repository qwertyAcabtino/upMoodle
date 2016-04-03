from django.db import models


class ErrorMessage(models.Model):
    id = models.AutoField(primary_key=True)
    error = models.CharField(max_length=200)
    http_code = models.IntegerField()

    def __unicode__(self):
        return self.error
