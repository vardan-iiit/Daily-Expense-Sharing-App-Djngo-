# Generated by Django 5.1.2 on 2024-10-21 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='split_details',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
