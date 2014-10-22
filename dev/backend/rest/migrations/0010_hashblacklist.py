# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0009_auto_20141019_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashBlackList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
