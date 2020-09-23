# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-05-01 11:27


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lti_edu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lticlient',
            name='issuer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='lti_client', to='issuer.Issuer'),
            preserve_default=False,
        ),
    ]
