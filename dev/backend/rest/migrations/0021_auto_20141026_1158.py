# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0020_calendarfrequency'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEventDate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('idEvent', models.ForeignKey(related_name=b'dates', to='rest.CalendarRegularEvent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='calendarregulareventdate',
            name='idEvent',
        ),
        migrations.DeleteModel(
            name='CalendarRegularEventDate',
        ),
        migrations.RemoveField(
            model_name='calendarsingleevent',
            name='author',
        ),
        migrations.RemoveField(
            model_name='calendarsingleevent',
            name='lastUpdated',
        ),
        migrations.RemoveField(
            model_name='calendarsingleevent',
            name='level',
        ),
        migrations.DeleteModel(
            name='CalendarSingleEvent',
        ),
        migrations.RemoveField(
            model_name='calendarregularevent',
            name='regular',
        ),
        migrations.AddField(
            model_name='calendarregularevent',
            name='frequency',
            field=models.ForeignKey(default=3, to='rest.CalendarFrequency'),
            preserve_default=True,
        ),
    ]
