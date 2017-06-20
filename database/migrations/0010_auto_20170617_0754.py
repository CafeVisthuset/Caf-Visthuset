# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20170611_1944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='day',
            options={'verbose_name': 'Dag', 'verbose_name_plural': 'Dagar'},
        ),
        migrations.AlterModelOptions(
            name='package',
            options={'verbose_name': 'Paket', 'verbose_name_plural': 'Paket'},
        ),
        migrations.AlterField(
            model_name='day',
            name='distance',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Hur långt cyklar man?'),
        ),
        migrations.AlterField(
            model_name='day',
            name='include_childbike',
            field=models.BooleanField(default=False, verbose_name='Ingår barncykel?'),
        ),
        migrations.AlterField(
            model_name='day',
            name='locks',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Hur många slussar?'),
        ),
        migrations.AlterField(
            model_name='day',
            name='lunch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lunch', to='database.Lunch'),
        ),
        migrations.AlterField(
            model_name='day',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='database.Rooms'),
        ),
        migrations.AlterField(
            model_name='package',
            name='image',
            field=models.ImageField(upload_to='static/img/uploads/', verbose_name='Bild'),
        ),
        migrations.AlterField(
            model_name='package',
            name='image_alt',
            field=models.CharField(blank=True, max_length=40, verbose_name='bildtext'),
        ),
        migrations.AlterField(
            model_name='package',
            name='targetgroup',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='targetgroup', to='database.Targetgroup', verbose_name='målgrupp'),
        ),
    ]
