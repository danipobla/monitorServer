# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cardiac', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='hrm',
        ),
        migrations.AddField(
            model_name='hrm',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cardiac.User'),
            preserve_default=False,
        ),
    ]
