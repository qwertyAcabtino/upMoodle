# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0010_hashblacklist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashblacklist',
            name='id',
        ),
        migrations.AlterField(
            model_name='hashblacklist',
            name='hash',
            field=models.CharField(max_length=2000, serialize=False, primary_key=True),
        ),
    ]
