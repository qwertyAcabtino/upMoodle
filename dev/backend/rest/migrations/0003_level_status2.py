# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_auto_20141019_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='status2',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
