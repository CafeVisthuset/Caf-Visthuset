# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-20 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0017_auto_20170620_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='guest', to='database.GuestProfile', verbose_name='gäst'),
        ),
    ]
