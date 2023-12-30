# Generated by Django 4.2 on 2023-12-29 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(default='6', on_delete=django.db.models.deletion.CASCADE, related_name='tickt_status', to='base.status'),
        ),
    ]