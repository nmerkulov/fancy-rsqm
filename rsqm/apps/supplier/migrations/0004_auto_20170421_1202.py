# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0003_auto_20170419_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='column_code',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='column_remain',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
