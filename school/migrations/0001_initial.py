# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(default='')),
                ('type', models.CharField(choices=[('L', 'Liste de mots'), ('T', 'Text')], default='T', max_length=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('niveau', models.PositiveSmallIntegerField(default=0, null=True)),
            ],
        ),
    ]
