# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-25 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20170410_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(upload_to='static/img/uploads/'),
        ),
    ]
