# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-18 21:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0003_auto_20170518_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='control_point',
        ),
        migrations.RemoveField(
            model_name='facilitydamage',
            name='control_point',
        ),
    ]
