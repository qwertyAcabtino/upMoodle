# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0025_auto_20141026_1253'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FileTags',
            new_name='FileTag',
        ),
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(default=datetime.date(2014, 10, 26), upload_to=b'files'),
            preserve_default=False,
        ),
    ]
