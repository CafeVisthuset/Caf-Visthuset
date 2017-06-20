# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-05 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0009_auto_20170519_1440'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facilitydamage',
            options={'ordering': ['-date'], 'verbose_name': 'Dokumentera fastighetsskada', 'verbose_name_plural': 'Dokumentera fastighetsskador'},
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='goods',
        ),
        migrations.AddField(
            model_name='delivery',
            name='note',
            field=models.CharField(default=' ', max_length=30, verbose_name='Följesedel'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='controlpoint',
            name='hazard',
        ),
        migrations.AddField(
            model_name='controlpoint',
            name='hazard',
            field=models.ManyToManyField(to='cleaning.Hazard'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='description',
            field=models.TextField(blank=True, max_length=200, verbose_name='beskrivning'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Epost'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=50, verbose_name='namn'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='other',
            field=models.TextField(blank=True, help_text='Till exempel att tänka på vid beställning', max_length=200, verbose_name='Övrigt'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.CharField(max_length=20, verbose_name='telefon'),
        ),
    ]
