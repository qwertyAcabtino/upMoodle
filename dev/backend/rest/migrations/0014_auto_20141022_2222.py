# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0013_auto_20141022_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarSingleEvent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=2000)),
                ('created', models.DateField(auto_now_add=True)),
                ('lastUpdate', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(related_name=b'single_lastUpdated', to='rest.User')),
                ('lastUpdated', models.ForeignKey(related_name=b'single_author', to='rest.User')),
                ('level', models.ForeignKey(to='rest.Level')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='calendarregularevent',
            name='author',
            field=models.ForeignKey(related_name=b'regular_lastUpdated', to='rest.User'),
        ),
        migrations.AlterField(
            model_name='calendarregularevent',
            name='lastUpdated',
            field=models.ForeignKey(related_name=b'regular_author', to='rest.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sessionDeadline',
            field=models.DateField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sessionToken',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
