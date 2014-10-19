# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0006_auto_20141019_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NoteBoard',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('topic', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=2000)),
                ('level', models.ForeignKey(to='rest.Level')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='level',
            old_name='status',
            new_name='visible',
        ),
        migrations.AlterField(
            model_name='level',
            name='type',
            field=models.ForeignKey(to='rest.LevelType'),
        ),
    ]
