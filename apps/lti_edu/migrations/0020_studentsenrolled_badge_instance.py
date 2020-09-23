# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-17 19:59


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0051_badgeinstance_public_key_issuer'),
        ('lti_edu', '0020_ltibadgeusertennant_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsenrolled',
            name='badge_instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='issuer.BadgeInstance'),
        ),
    ]
