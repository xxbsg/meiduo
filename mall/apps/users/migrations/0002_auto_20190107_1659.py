# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-07 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='moibls',
            new_name='mobile',
        ),
    ]
