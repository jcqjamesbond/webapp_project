# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-20 19:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Meal', 'Meal'), ('Movie', 'Movie'), ('Drink', 'Drink'), ('Party', 'Party')], default='meal', max_length=30)),
                ('city', models.CharField(default='Pittsburgh', max_length=100)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_changed', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('gender', models.CharField(blank=True, default='', max_length=20)),
                ('age', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
                ('bio', models.CharField(blank=True, default='Write your short bio here.', max_length=420)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.ImageField(blank=True, upload_to='profile_pictures')),
                ('phone', models.PositiveSmallIntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='followers',
            field=models.ManyToManyField(related_name='following_event', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
