# Generated by Django 2.2.9 on 2020-03-24 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_populate_entity_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgeclassstaff',
            name='entity_id',
            field=models.CharField(default=None, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='facultystaff',
            name='entity_id',
            field=models.CharField(default=None, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='institutionstaff',
            name='entity_id',
            field=models.CharField(default=None, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='issuerstaff',
            name='entity_id',
            field=models.CharField(default=None, max_length=254, unique=True),
        ),
    ]
