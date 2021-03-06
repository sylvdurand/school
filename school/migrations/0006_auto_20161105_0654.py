# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20161030_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictee',
            name='niveau',
            field=models.PositiveSmallIntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='dictee',
            name='type',
            field=models.CharField(choices=[('L', 'Liste de mots'), ('T', 'Text')], default='L', max_length=1),
        ),
        migrations.AlterField(
            model_name='probleme',
            name='title',
            field=models.TextField(max_length=200),
        ),
    ]
