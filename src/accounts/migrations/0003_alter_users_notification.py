# Generated by Django 5.1.7 on 2025-03-12 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "accounts",
            "0002_users_division_users_notification_users_number_phone_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="notification",
            field=models.JSONField(
                blank=True, default=dict, null=True, verbose_name="Уведомление"
            ),
        ),
    ]
