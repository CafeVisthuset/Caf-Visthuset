# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-19 14:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0006_auto_20170518_2215'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Clean',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='facilitydamage',
            name='signature',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='control_point',
        ),
        migrations.RemoveField(
            model_name='temperature',
            name='signature',
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
        migrations.DeleteModel(
            name='FacilityDamage',
        ),
        migrations.DeleteModel(
            name='Temperature',
        ),
    ]
