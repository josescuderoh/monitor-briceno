# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20171109_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='beneficiary',
            field=models.CharField(choices=[('Individuos', 'Individuos'), ('Instituciones', 'Instituciones'), ('Familias', 'Familias')], max_length=30, verbose_name='Tipo de destinatario'),
        ),
        migrations.AlterField(
            model_name='project',
            name='beneficiary_comments',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones sobre los destinatarios'),
        ),
        migrations.AlterField(
            model_name='project',
            name='no_benef',
            field=models.IntegerField(verbose_name='Número de destinatarios'),
        ),
    ]