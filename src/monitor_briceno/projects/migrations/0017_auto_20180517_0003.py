# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-17 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20180516_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.IntegerField(default=0, help_text='Cifra en pesos colombianos', verbose_name='Monto de ejecución'),
        ),
    ]