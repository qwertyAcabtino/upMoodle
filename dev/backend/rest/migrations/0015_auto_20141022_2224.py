# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0014_auto_20141022_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sessionDeadline',
        ),
        migrations.AlterField(
            model_name='user',
            name='sessionToken',
            field=models.CharField(max_length=1000),
        ),
    ]
