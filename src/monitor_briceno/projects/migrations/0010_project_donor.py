# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20171109_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='donor',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Donante'),
        ),
    ]
