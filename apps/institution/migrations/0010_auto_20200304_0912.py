# Generated by Django 2.2.9 on 2020-03-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0009_auto_20200302_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='entity_id',
            field=models.CharField(default=None, max_length=254, unique=False, null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='entity_version',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
