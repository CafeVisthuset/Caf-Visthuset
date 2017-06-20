# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-10 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_auto_20170605_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='BikeSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Namn')),
                ('internal', models.CharField(max_length=25, verbose_name='Internt namn')),
                ('min_age', models.PositiveIntegerField(verbose_name='Minimum ålder')),
                ('max_age', models.PositiveIntegerField(blank=True, verbose_name='Max ålder')),
                ('wheelsize', models.PositiveIntegerField(verbose_name='Däckdiameter')),
            ],
        ),
        migrations.AlterModelOptions(
            name='bike',
            options={'ordering': ['number'], 'verbose_name': 'cykel', 'verbose_name_plural': 'cyklar'},
        ),
        migrations.RemoveField(
            model_name='day',
            name='adult_bike',
        ),
        migrations.RemoveField(
            model_name='day',
            name='child_bike',
        ),
        migrations.AddField(
            model_name='day',
            name='include_childbike',
            field=models.PositiveIntegerField(blank=True, default=False, verbose_name='Ingår barncykel?'),
        ),
        migrations.AddField(
            model_name='day',
            name='inlcude_adultbike',
            field=models.BooleanField(default=True, verbose_name='Ingår vuxencykel?'),
        ),
        migrations.AddField(
            model_name='roomsbooking',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Bekräftad av anläggningen?'),
        ),
        migrations.AddField(
            model_name='roomsbooking',
            name='facility_booking',
            field=models.CharField(blank=True, max_length=25, verbose_name='Anläggningens bokningsnummer'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='package',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='database.Package', verbose_name='Paket'),
        ),
        migrations.AlterUniqueTogether(
            name='bike',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bike',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='bike',
            name='rentOutCount',
        ),
        migrations.RemoveField(
            model_name='bike',
            name='wheelsize',
        ),
        migrations.AddField(
            model_name='bike',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='size', to='database.BikeSize', verbose_name='storlek'),
            preserve_default=False,
        ),
    ]
