# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-22 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0003_auto_20161220_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='pole',
            name='ilosc',
            field=models.IntegerField(default=0),
        ),
    ]
