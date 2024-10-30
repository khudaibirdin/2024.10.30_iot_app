# Generated by Django 5.1.1 on 2024-09-25 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('web_app', '0003_delete_journal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('code', models.CharField(max_length=250)),
                ('variable_name', models.CharField(max_length=250)),
                ('message', models.CharField(max_length=250)),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.filial')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.location')),
            ],
        ),
    ]
