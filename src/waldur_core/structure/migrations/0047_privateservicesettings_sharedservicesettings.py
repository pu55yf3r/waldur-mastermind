# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-07 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0046_shared_service_settings_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateServiceSettings',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Private provider settings',
            },
            bases=('structure.servicesettings',),
        ),
        migrations.CreateModel(
            name='SharedServiceSettings',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Shared provider settings',
            },
            bases=('structure.servicesettings',),
        ),
    ]