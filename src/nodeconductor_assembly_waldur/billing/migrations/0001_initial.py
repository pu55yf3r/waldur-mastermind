# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-06 13:28
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import nodeconductor.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', nodeconductor.core.fields.UUIDField()),
                ('threshold', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('total', models.FloatField(default=0, help_text='Predicted price for scope for current month.')),
                ('limit', models.FloatField(default=-1, help_text='How many funds object can consume in current month.-1 means no limit.')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
