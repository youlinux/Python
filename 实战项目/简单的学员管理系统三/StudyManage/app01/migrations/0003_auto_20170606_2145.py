# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 13:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20170604_1528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_customer_list', '可以查看客户列表'), ('view_customer_info', '可以查看客户详情'), ('edit_own_customer_info', '可以修改自己的客户详情')), 'verbose_name': '员工信息表', 'verbose_name_plural': '员工信息表'},
        ),
    ]
