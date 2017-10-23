# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import entities.models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_auto_20171004_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='organization_logo',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=entities.models.upload_location, width_field='width_field'),
        ),
    ]
