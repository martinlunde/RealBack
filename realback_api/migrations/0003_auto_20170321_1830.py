# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 17:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realback_api', '0002_auto_20170314_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)])),
                ('understanding', models.IntegerField(default=0)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AddField(
            model_name='lecturetopic',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realback_api.Lecture'),
        ),
    ]