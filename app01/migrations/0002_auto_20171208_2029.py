# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_userinfo_date',
            name='date',
            field=models.DateField(verbose_name='日期'),
        ),
    ]
