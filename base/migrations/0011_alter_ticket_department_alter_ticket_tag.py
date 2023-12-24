# Generated by Django 4.2 on 2023-12-25 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_ticket_department_ticket_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickt_department', to='base.department'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickt_tag', to='base.tag'),
        ),
    ]