# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0007_auto_20141019_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leveltype',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
