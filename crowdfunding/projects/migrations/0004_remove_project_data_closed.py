# Generated by Django 5.1 on 2024-09-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_data_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='data_closed',
        ),
    ]
