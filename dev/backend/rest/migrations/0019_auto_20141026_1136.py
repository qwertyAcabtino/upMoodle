# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0018_auto_20141022_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarregulareventdate',
            name='idEvent',
            field=models.ForeignKey(related_name=b'dates', to='rest.CalendarRegularEvent'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(upload_to=b'pics/users', blank=True),
        ),
    ]
