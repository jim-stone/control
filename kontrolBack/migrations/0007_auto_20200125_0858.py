# Generated by Django 2.2.7 on 2020-01-25 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kontrolBack', '0006_auto_20200124_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kontrolBack.QuestionInList'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('question', 'content')},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='control',
        ),
    ]
