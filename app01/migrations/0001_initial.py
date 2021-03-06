# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='会议室名称')),
            ],
            options={
                'verbose_name_plural': '会议室',
            },
        ),
        migrations.CreateModel(
            name='Room_userinfo_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='日期')),
                ('time', models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00'), (11, '18:00'), (12, '19:00'), (13, '20:00')], verbose_name='时间段')),
            ],
            options={
                'verbose_name_plural': '时间日期用户',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AddField(
            model_name='room_userinfo_date',
            name='UserInfo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='room_userinfo_date',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Room', verbose_name='会议室'),
        ),
    ]
