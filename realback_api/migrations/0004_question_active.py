# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realback_api', '0003_lecture_active_topic_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]