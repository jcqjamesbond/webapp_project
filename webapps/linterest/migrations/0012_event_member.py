# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-05 05:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linterest', '0011_auto_20161204_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='member',
            field=models.ManyToManyField(related_name='event_member', to='linterest.Profile'),
        ),
    ]