# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0023_auto_20141026_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendareventdate',
            old_name='hour',
            new_name='hourEnd',
        ),
        migrations.AddField(
            model_name='calendareventdate',
            name='hourStart',
            field=models.TimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='calendareventdate',
            name='allDay',
            field=models.BooleanField(default=False),
        ),
    ]
