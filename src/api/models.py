from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        abstract = True


class Project(BaseModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Создатель проекта",
        related_name="owned_project",
    )
    members = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Участники",
        blank=True,
        null=True,
        related_name="projects",
    )


class Board(BaseModel):
    STATUS_CHOICES = [
        ("backlog", "Бэклог"),
        ("in_progress", "В работе"),
        ("testing", "Тестирование"),
        ("completed", "Завершено"),
    ]

    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, verbose_name="Проект"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="backlog", verbose_name="Статус"
    )


class Task(BaseModel):
    PRIORITY_CHOICES = [
        ("high", "Высокий"),
        ("medium", "Средний"),
        ("low", "Низкий"),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="Доска")
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


class AdditionalTask(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, verbose_name="Дополнительная задача"
    )

    def __str__(self):
        return self.title


class ProjectMemberShip(models.Model):
    ROLES_CHOICES = [
        ("owner", "Создатель"),
        ("admin", "Администратор"),
        ("member", "Участник"),
        ("viewer", "Зритель"),
    ]
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name="Исполнители")
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, verbose_name="Проект"
    )
    role = models.CharField(
        max_length=20, choices=ROLES_CHOICES, default="member", verbose_name="Роли"
    )


class TaskRelation(models.Model):
    RELATION_TYPES = [
        ("block", "Block"),
        ("relates_to", "Relates To"),
        ("duplicates", "Duplicates"),
    ]
    from_task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=True, related_name="from_relations"
    )
    to_task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=True, related_name="to_relations"
    )
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES, blank=True)
