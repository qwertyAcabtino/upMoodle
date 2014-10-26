# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0024_auto_20141026_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('hash', models.CharField(max_length=65)),
                ('name', models.CharField(max_length=100)),
                ('fileType', models.CharField(max_length=50)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('visible', models.BooleanField(default=True)),
                ('lastUpdater', models.ForeignKey(related_name=b'file_updater', to='rest.User')),
                ('subject', models.ForeignKey(to='rest.Level')),
                ('uploader', models.ForeignKey(related_name=b'file_lastUpdater', to='rest.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileComments',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=1000)),
                ('idAuthor', models.ForeignKey(to='rest.User')),
                ('idFile', models.ForeignKey(to='rest.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileReportList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=200)),
                ('idFile', models.ForeignKey(to='rest.File')),
                ('idReporter', models.ForeignKey(to='rest.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idFile', models.ForeignKey(to='rest.File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('verbose', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filetags',
            name='idTag',
            field=models.ForeignKey(to='rest.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='file',
            name='year',
            field=models.ForeignKey(to='rest.Year'),
            preserve_default=True,
        ),
    ]
