# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_level_status2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='status2',
        ),
    ]
