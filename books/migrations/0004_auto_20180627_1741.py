# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-27 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20180609_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passwd',
            field=models.CharField(max_length=200, verbose_name='密码'),
        ),
    ]