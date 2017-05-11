# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-06 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0008_auto_20170506_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecontent',
            name='order',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], default=1, help_text='1 är innehåll högt upp på sidan, 4 långt ner'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='headline',
            field=models.CharField(blank=True, help_text='kort H2-rubrik, ex "riktigt gott kaffe"', max_length=100),
        ),
    ]
