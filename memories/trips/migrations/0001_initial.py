# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-14 02:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='', max_length=20)),
                ('state', models.CharField(default='', max_length=30)),
                ('city', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat_lng', geoposition.fields.GeopositionField(max_length=42)),
                ('file_path', models.CharField(max_length=200)),
                ('file_path_real', models.CharField(max_length=240)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Location')),
            ],
        ),
    ]
