# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_auto_20170617_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='lunch',
            name='type',
            field=models.CharField(choices=[(None, 'övrigt'), ('picnic', 'Picknicklunch')], max_length=15, null=True, verbose_name='lunchtyp'),
        ),
    ]
