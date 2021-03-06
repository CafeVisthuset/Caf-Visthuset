# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20170617_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lunch',
            name='internal',
        ),
        migrations.AlterField(
            model_name='lunch',
            name='name',
            field=models.CharField(help_text='Namn att visa utåt', max_length=30, verbose_name='Lunch'),
        ),
        migrations.AlterField(
            model_name='lunch',
            name='slug',
            field=models.SlugField(default='', help_text='Namn att använda i koden, ändra inte!!', verbose_name='Internt namn'),
        ),
    ]
