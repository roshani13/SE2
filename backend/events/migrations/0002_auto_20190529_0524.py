# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-29 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
