# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0016_auto_20141022_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarregularevent',
            name='regular',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
