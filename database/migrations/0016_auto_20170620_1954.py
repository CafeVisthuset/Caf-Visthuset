# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-20 19:54
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0015_auto_20170618_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsletter', models.BooleanField(default=True)),
                ('phone_number', models.CharField(blank=True, max_length=24, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'gäster',
                'verbose_name': 'gäst',
            },
        ),
        migrations.DeleteModel(
            name='PackageBooking',
        ),
        migrations.AlterField(
            model_name='bikesbooking',
            name='bike',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bike', to='database.Bike', verbose_name='Cykel'),
        ),
        migrations.AlterField(
            model_name='bikesbooking',
            name='duration',
            field=models.DurationField(choices=[(datetime.timedelta(1), '1 Dag'), (datetime.timedelta(2), '2 Dagar'), (datetime.timedelta(3), '3 Dagar'), (datetime.timedelta(4), '4 Dagar'), (datetime.timedelta(5), '5 Dagar'), (datetime.timedelta(6), '6 Dagar'), (datetime.timedelta(7), '7 Dagar')], default=datetime.timedelta(1), verbose_name='Hur många dagar?'),
        ),
        migrations.AlterField(
            model_name='bikesbooking',
            name='from_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Från datum'),
        ),
        migrations.AlterField(
            model_name='bikesbooking',
            name='to_date',
            field=models.DateField(blank=True, default=datetime.date.today, verbose_name='Till datum'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('cancl', 'Avbokad'), ('actv', 'Aktiv'), ('cmplt', 'Genomförd'), ('prel', 'Preliminär'), ('unconf', 'Obekräftad')], max_length=5, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='lunchbooking',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_lunches', to='database.Booking', verbose_name='Bokning'),
        ),
        migrations.AlterField(
            model_name='lunchbooking',
            name='day',
            field=models.DateField(verbose_name='dag'),
        ),
        migrations.AlterField(
            model_name='lunchbooking',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='kvantitet'),
        ),
        migrations.AlterField(
            model_name='lunchbooking',
            name='type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='database.Lunch', verbose_name='Lunchtyp'),
        ),
        migrations.AlterField(
            model_name='roomsbooking',
            name='from_date',
            field=models.DateField(verbose_name='incheckning'),
        ),
        migrations.AlterField(
            model_name='roomsbooking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Rooms', verbose_name='Rum'),
        ),
        migrations.AlterField(
            model_name='roomsbooking',
            name='to_date',
            field=models.DateField(verbose_name='utcheckning'),
        ),
    ]