# Generated by Django 5.1.7 on 2025-03-20 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_users_number_phone_verificationcode"),
    ]

    operations = [
        migrations.DeleteModel(
            name="VerificationCode",
        ),
    ]
