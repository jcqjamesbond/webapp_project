# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-04 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linterest', '0006_chatroom_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
