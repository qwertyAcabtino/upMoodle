# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0012_auto_20141022_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarRegularEvent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=2000)),
                ('created', models.DateField(auto_now_add=True)),
                ('lastUpdate', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CalendarRegularEventDate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('idEvent', models.ForeignKey(to='rest.CalendarRegularEvent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=100)),
                ('nick', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('profilePic', models.ImageField(upload_to=b'users')),
                ('lastTimeActive', models.DateField(auto_now=True)),
                ('joined', models.DateField(auto_now_add=True)),
                ('banned', models.BooleanField(default=False)),
                ('sessionToken', models.CharField(max_length=1000)),
                ('sessionDeadline', models.DateField()),
                ('rol', models.ForeignKey(to='rest.Rol')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='calendarregularevent',
            name='author',
            field=models.ForeignKey(related_name=b'lastUpdated', to='rest.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendarregularevent',
            name='lastUpdated',
            field=models.ForeignKey(related_name=b'author', to='rest.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendarregularevent',
            name='level',
            field=models.ForeignKey(to='rest.Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bannedhash',
            name='hash',
            field=models.CharField(max_length=65, serialize=False, primary_key=True),
        ),
    ]
