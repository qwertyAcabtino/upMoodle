# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0011_auto_20141022_2117'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HashBlackList',
            new_name='BannedHash',
        ),
    ]
