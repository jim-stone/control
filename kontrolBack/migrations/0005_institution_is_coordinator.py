# Generated by Django 2.2.7 on 2020-01-24 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrolBack', '0004_auto_20200124_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='is_coordinator',
            field=models.BooleanField(default=False),
        ),
    ]
