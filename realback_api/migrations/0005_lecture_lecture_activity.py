# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realback_api', '0004_lecture_attendee_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='lecture_activity',
            field=models.IntegerField(default=0),
        ),
    ]
