# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('realback_api', '0007_merge_20170322_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='pace_reset_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lecture',
            name='volume_reset_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]