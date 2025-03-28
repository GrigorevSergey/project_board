# Generated by Django 5.1.7 on 2025-03-11 05:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="members",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Участники",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_project",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Создатель проекта",
            ),
        ),
    ]
