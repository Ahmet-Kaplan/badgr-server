# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-19 11:13


from django.db import migrations

from entity.db.migrations import PopulateEntityIdsMigration


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0003_faculty_entity_id'),
    ]

    operations = [
        PopulateEntityIdsMigration('institution', 'Faculty'),
    ]