# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-30 09:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_creatednotes_createdreminders_notes_reminderdetails'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reminderdetails',
            old_name='reminder_name',
            new_name='title',
        ),
    ]