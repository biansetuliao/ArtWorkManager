# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-23 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160421_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
