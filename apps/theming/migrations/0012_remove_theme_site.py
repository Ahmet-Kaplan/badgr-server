# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-04 10:33


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theming', '0011_theme_terms_and_conditions_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='site',
        ),
    ]