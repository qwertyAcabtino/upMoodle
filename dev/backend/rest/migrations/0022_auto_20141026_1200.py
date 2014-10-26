# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0021_auto_20141026_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendareventdate',
            name='date',
        ),
        migrations.AddField(
            model_name='calendareventdate',
            name='index',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
