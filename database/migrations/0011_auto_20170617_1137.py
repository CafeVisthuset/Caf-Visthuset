# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 11:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20170617_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.Package', verbose_name='Paket'),
        ),
    ]