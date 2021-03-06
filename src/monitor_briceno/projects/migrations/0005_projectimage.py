# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 19:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20171004_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=projects.models.upload_location)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='projects.Project')),
            ],
        ),
    ]
