# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-11-13 14:44


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issuer', '0050_badgeinstance_identifier'),
        ('signing', '0002_remove_privatekey_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssertionTimeStamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=64)),
                ('original_json', models.TextField()),
                ('hash_id_nodes', models.TextField(default=None, null=True)),
                ('proof', models.TextField()),
                ('badge_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuer.BadgeInstance')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicKeyIssuer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_version', models.PositiveIntegerField(default=1)),
                ('entity_id', models.CharField(default=None, max_length=254, unique=True)),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issuer.Issuer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='publickey',
            name='issuer',
        ),
        migrations.AlterField(
            model_name='symmetrickey',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publickeyissuer',
            name='public_key',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='signing.PublicKey'),
        ),
    ]