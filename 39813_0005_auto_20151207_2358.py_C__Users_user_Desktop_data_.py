# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-07 23:58
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsourcing', '0004_batchfile_hash_sha512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchfile',
            name='first_row',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
