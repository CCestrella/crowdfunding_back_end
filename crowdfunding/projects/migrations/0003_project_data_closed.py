# Generated by Django 5.1 on 2024-09-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='data_closed',
            field=models.DateTimeField(null=True),
        ),
    ]
