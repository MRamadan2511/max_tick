# Generated by Django 4.2 on 2023-11-26 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_location_alter_ticket_warehouse_delete_warehouse'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]