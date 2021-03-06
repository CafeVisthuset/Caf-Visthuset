# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-01 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='numberOfGuests',
        ),
        migrations.AddField(
            model_name='booking',
            name='adults',
            field=models.IntegerField(default=2, verbose_name='antal vuxna'),
        ),
        migrations.AddField(
            model_name='booking',
            name='children',
            field=models.IntegerField(default=0, null=True, verbose_name='antal barn'),
        ),
    ]
