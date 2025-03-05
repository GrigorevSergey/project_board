from django.conf import settings
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")


class Board(models.Model):
    STATUS_CHOICES = [
        ("backlog", "Бэклог"),
        ("in_progress", "В работе"),
        ("testing", "Тестирование"),
        ("completed", "Завершено"),
    ]

    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, verbose_name="Проект"
    )
    title = models.CharField(max_length=100, verbose_name="Название")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="backlog", verbose_name="Статус"
    )


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("high", "Высокий"),
        ("medium", "Средний"),
        ("low", "Низкий"),
    ]
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="Доска")
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание задачи")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Исполнители")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="low", verbose_name="Приоритет"
    )
    date_completion = models.DateTimeField(
        null=True, blank=True, verbose_name="Срок выполнения"
    )
    completed_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата выполнения"
    )

    def __str__(self):
        return self.title


class AdditionalTask(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name="Дополнительная задача"
    )
    title = models.CharField(max_length=100, verbose_name="Название доп.задачи")
    description = models.TextField(verbose_name="Описание доп.задачи")

    def __str__(self):
        return self.title
