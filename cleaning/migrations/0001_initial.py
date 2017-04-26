# -*- coding: utf-8 -*-
<<<<<<< HEAD
# Generated by Django 1.10.6 on 2017-04-26 22:13
=======
# Generated by Django 1.10.4 on 2017-04-26 21:56
>>>>>>> master
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Economy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
=======
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('hazard', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('damaged', models.BooleanField(default=False)),
                ('expired', models.BooleanField(default=False)),
                ('anomaly', models.BooleanField(default=False)),
                ('signature', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Economy.Employee')),
            ],
            options={
                'verbose_name': 'leverans',
                'verbose_name_plural': 'leveranser',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
>>>>>>> master
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clean', models.BooleanField(default=False)),
                ('open', models.BooleanField(default=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('signature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Economy.Employee')),
            ],
            options={
<<<<<<< HEAD
                'verbose_name': 'Golv',
                'verbose_name_plural': 'Golven',
=======
                'verbose_name_plural': 'Golven',
                'verbose_name': 'Golv',
>>>>>>> master
            },
        ),
        migrations.CreateModel(
            name='Freezer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Typ av frys')),
                ('location', models.CharField(max_length=255, verbose_name='Plats')),
                ('active', models.BooleanField(default=True, verbose_name='Är den aktiv?')),
            ],
            options={
                'verbose_name': 'Frys',
                'verbose_name_plural': 'Frysar',
                'ordering': ['-active'],
            },
        ),
        migrations.CreateModel(
            name='FreezerTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measured', models.IntegerField(verbose_name='Uppmätt temperatur')),
                ('defrosted', models.BooleanField(default=False, verbose_name='Avfrostad')),
                ('anomaly', models.BooleanField(default=False, verbose_name='avvikelse')),
                ('cleaned', models.BooleanField(verbose_name='Städat')),
                ('comment', models.TextField(blank=True, max_length=255, verbose_name='kommentar')),
                ('prescribedMaxTempFridge', models.PositiveIntegerField(default=8)),
                ('prescribedMinTempFridge', models.PositiveIntegerField(default=4)),
                ('prescribedMaxTempFreezer', models.IntegerField(default=-4)),
                ('prescribedMinTempFreezer', models.IntegerField(default=-20)),
                ('date', models.DateField(default=datetime.date.today)),
                ('signature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Economy.Employee', verbose_name='Signatur')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cleaning.Freezer', verbose_name='Typ av frys')),
            ],
            options={
                'verbose_name': 'Kontrollpunkt frys',
                'verbose_name_plural': 'Kontrollpunkter frysar',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Typ av kyl')),
                ('location', models.CharField(max_length=255, verbose_name='Plats')),
                ('active', models.BooleanField(default=True, verbose_name='Är den aktiv?')),
            ],
            options={
                'verbose_name': 'Kyl',
                'verbose_name_plural': 'Kylar',
                'ordering': ['-active'],
            },
        ),
        migrations.CreateModel(
            name='FridgeTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measured', models.IntegerField(verbose_name='Uppmätt temperatur')),
                ('defrosted', models.BooleanField(default=False, verbose_name='Avfrostad')),
                ('anomaly', models.BooleanField(default=False, verbose_name='avvikelse')),
                ('cleaned', models.BooleanField(verbose_name='Städat')),
                ('comment', models.TextField(blank=True, max_length=255, verbose_name='kommentar')),
                ('prescribedMaxTempFridge', models.PositiveIntegerField(default=8)),
                ('prescribedMinTempFridge', models.PositiveIntegerField(default=4)),
                ('prescribedMaxTempFreezer', models.IntegerField(default=-4)),
                ('prescribedMinTempFreezer', models.IntegerField(default=-20)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='datum')),
                ('signature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Economy.Employee', verbose_name='Signatur')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cleaning.Fridge', verbose_name='Enhet')),
            ],
            options={
                'verbose_name': 'Kontrollpunkt kylskåp',
                'verbose_name_plural': 'Kontrollpunkter kylskåp',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
<<<<<<< HEAD
=======
            name='Ingredience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, help_text='Pris/kg eller pris/l', max_digits=6)),
                ('package_size', models.CharField(blank=True, help_text='storlek på paket, om standard. Ex. 25 kg säck', max_length=30)),
                ('allergen', models.ManyToManyField(to='cleaning.Allergen')),
            ],
            options={
                'verbose_name_plural': 'ingredienser',
                'verbose_name': 'ingrediens',
            },
        ),
        migrations.CreateModel(
>>>>>>> master
            name='Kitchen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clean', models.BooleanField(default=False)),
                ('open', models.BooleanField(default=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('signature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Economy.Employee')),
            ],
            options={
                'verbose_name': 'Köket',
            },
        ),
<<<<<<< HEAD
=======
        migrations.CreateModel(
            name='Recepie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pieces', models.IntegerField(help_text='Antal per sats')),
                ('customer_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('retailer_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('work_hours', models.DurationField(help_text='Arbetsinsats för en sats')),
                ('oven_time', models.DurationField(help_text='Tid i ugnen')),
                ('description', models.TextField(help_text='Hur gör man?', max_length=1000)),
                ('added', models.TimeField(auto_now_add=True)),
                ('updated', models.TimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'recept',
                'verbose_name_plural': 'recept',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RecepieIngredience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredience', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cleaning.Ingredience')),
                ('recepie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cleaning.Recepie')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contact', models.CharField(max_length=30, verbose_name='kontaktperson')),
                ('order_day', models.CharField(choices=[('monday', 'Måndag'), ('tuesday', 'Tisdag'), ('wednesday', 'Onsdag'), ('thursday', 'Torsdag'), ('friday', 'Fredag'), ('saturday', 'Lördag'), ('sunday', 'Söndag')], help_text='Veckodag för beställning', max_length=15)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('goods', models.TextField(blank=True, max_length=100)),
                ('other', models.TextField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'leverantörer',
                'verbose_name': 'leverantör',
            },
        ),
        migrations.AddField(
            model_name='ingredience',
            name='supplier',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='cleaning.Supplier'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cleaning.Supplier'),
        ),
>>>>>>> master
    ]
