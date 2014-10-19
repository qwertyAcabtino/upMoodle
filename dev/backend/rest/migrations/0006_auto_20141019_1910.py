# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0005_auto_20141019_1819'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Levels',
            new_name='Level',
        ),
        migrations.RenameField(
            model_name='level',
            old_name='level',
            new_name='type',
        ),
    ]
