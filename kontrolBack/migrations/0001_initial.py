# Generated by Django 2.2.7 on 2020-01-23 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.IntegerField(choices=[(0, 'tak'), (1, 'nie'), (2, 'nie dotyczy')])),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'w przygotowaniu'), (1, 'w trakcie'), (2, 'w procesie zgłaszania uwag do wyniku'), (3, 'zakończona')], default=0)),
                ('checklist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='controls', to='kontrolBack.Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=512)),
                ('name', models.CharField(max_length=512)),
                ('beneficiary_name', models.CharField(max_length=512)),
                ('beneficiary_nip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionInList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=500)),
                ('block_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ResultInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='kontrolBack.Control')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=10000)),
                ('result_info', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recommendations', to='kontrolBack.ResultInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, unique=True)),
                ('order_in_block', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='kontrolBack.QuestionBlock')),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kontrolBack.Institution')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Finding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=10000)),
                ('result_info', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='findings', to='kontrolBack.ResultInfo')),
            ],
        ),
        migrations.AddField(
            model_name='control',
            name='controlling',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='controls_by', to='kontrolBack.Institution'),
        ),
        migrations.AddField(
            model_name='control',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='controls_at_project', to='kontrolBack.Project'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='kontrolBack.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='checklist',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='checklists', to='kontrolBack.InstitutionEmployee'),
        ),
        migrations.AddField(
            model_name='answer',
            name='control',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='kontrolBack.Control'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='kontrolBack.QuestionInList'),
        ),
    ]