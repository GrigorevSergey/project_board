# Generated by Django 5.1.7 on 2025-03-24 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_verificationcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
