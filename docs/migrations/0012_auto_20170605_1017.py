# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-05 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('docs', '0011_banner_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Skapad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='banner',
            name='internal',
            field=models.CharField(blank=True, max_length=40, verbose_name='Internt namn'),
        ),
        migrations.AddField(
            model_name='banner',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Uppdaterad'),
        ),
        migrations.AddField(
            model_name='page',
            name='code',
            field=models.SlugField(default='', help_text='sidans namn att använda i koden, e.g., "index"', verbose_name='Kod'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='banner',
            name='publish',
            field=models.BooleanField(default=False, verbose_name='Publicera'),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Namn'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='page',
            field=models.ForeignKey(blank=True, help_text='På vilken sida vill du publicera detta?', on_delete=django.db.models.deletion.DO_NOTHING, to='docs.Page'),
        ),
    ]
