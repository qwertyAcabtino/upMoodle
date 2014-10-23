# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0015_auto_20141022_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(upload_to=b'users', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sessionToken',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
