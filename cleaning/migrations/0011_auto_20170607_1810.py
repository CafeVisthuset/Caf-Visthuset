# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-07 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0010_auto_20170605_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routine_recurr', models.CharField(choices=[('yearly', 'Årligen'), ('monthly', 'Månadsvis'), ('weekly', 'Veckovis'), ('2week', '2 ggr/vecka'), ('3week', '3 ggr/vecka'), ('daily', 'Dagligen'), ('always', 'Vid varje tillfälle')], max_length=15, verbose_name='Hur ofta utförs rutinen?')),
                ('routine_sufficient', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, max_length=200, verbose_name='kommentar')),
            ],
        ),
        migrations.RemoveField(
            model_name='controlpoint',
            name='routine',
        ),
        migrations.AlterField(
            model_name='controlpoint',
            name='hazard',
            field=models.ManyToManyField(to='cleaning.Hazard', verbose_name='Fara'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='control_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleaning.ControlPoint', verbose_name='kontrollpunkt'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='routine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cleaning.Routine', verbose_name='Rutin'),
        ),
    ]
