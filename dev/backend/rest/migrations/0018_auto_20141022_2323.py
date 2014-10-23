# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0017_calendarregularevent_regular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarregulareventdate',
            name='idEvent',
            field=models.ForeignKey(related_name=b'idEvent', to='rest.CalendarRegularEvent'),
        ),
    ]
