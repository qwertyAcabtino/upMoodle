# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0022_auto_20141026_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarregularevent',
            name='frequency',
        ),
        migrations.AddField(
            model_name='calendareventdate',
            name='allDay',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendareventdate',
            name='frequency',
            field=models.ForeignKey(default=4, to='rest.CalendarFrequency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendareventdate',
            name='hour',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
    ]
