# Generated by Django 2.2.7 on 2020-01-23 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kontrolBack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioninlist',
            name='checklist',
            field=models.ManyToManyField(related_name='questions', to='kontrolBack.Checklist'),
        ),
    ]
