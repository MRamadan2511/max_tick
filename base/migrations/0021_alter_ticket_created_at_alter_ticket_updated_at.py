# Generated by Django 4.2 on 2024-01-01 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 1, 19, 57, 38, 644342)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 1, 19, 57, 38, 644342)),
        ),
    ]