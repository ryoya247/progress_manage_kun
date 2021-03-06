# Generated by Django 2.1.3 on 2018-12-08 19:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20181114_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_progress', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='進捗プラス')),
                ('text', models.TextField(default='例：Taskモデルを作った', max_length=400, verbose_name='やったこと')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='期限'),
        ),
        migrations.AlterField(
            model_name='task',
            name='progress',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='進捗'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=60, verbose_name='タスク名'),
        ),
        migrations.AddField(
            model_name='report',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task'),
        ),
    ]
