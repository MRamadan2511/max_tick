# Generated by Django 4.2 on 2024-01-01 20:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_ticket_created_at_alter_ticket_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
