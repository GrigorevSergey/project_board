from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    AdditionalTask,
    Board,
    Project,
    ProjectMemberShip,
    Task,
    TaskRelation,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "members_count", "description")
    list_filter = ("title",)
    search_fields = ("title", "description")
    filter_horizontal = ("members",)

    def owner(self, obj):
        if obj.owner:
            return obj.owner
        return "-"

    def members_count(self, obj):
        return obj.members.count()

    members_count.short_description = "Участников"


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "project_admin", "status", "task_count", "percentage")
    list_filter = ("status", "project")
    search_fields = ("title", "project__title")
    readonly_fields = ("percentage",)

    def project_admin(self, obj):
        return obj.project.title

    project_admin.short_description = "Проект"

    def task_count(self, obj):
        return obj.task_set.count()

    task_count.short_description = "Всего задач"

    def percentage(self, obj):
        total = obj.task_set.count()
        completed = obj.task_set.filter(board__status="completed").count()
        return f"{completed / total * 100}%" if total > 0 else "0%"

    percentage.short_description = "Выполнено"


class AdditionalTaskInline(admin.TabularInline):
    model = AdditionalTask
    extra = 1
    fields = ("title", "description")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "board_admin",
        "priority",
        "status",
        "date_completion",
        "is_overdue",
        "assigned_users",
    )
    list_filter = ("priority", "board__status", "date_completion")
    search_fields = ("title", "description")
    filter_horizontal = ("users",)
    inlines = [AdditionalTaskInline]

    def board_admin(self, obj):
        return obj.board.title

    board_admin.short_description = "Доска"

    def status(self, obj):
        return obj.board.get_status_display()

    status.short_description = "Статус"

    def is_overdue(self, obj):
        if obj.date_completion:
            return obj.date_completion < timezone.now()
        return False

    is_overdue.boolean = True
    is_overdue.short_description = "Просрочено"

    def assigned_users(self, obj):
        return ", ".join([x.username for x in obj.users.all()])

    assigned_users.short_description = "Исполнители"


@admin.register(ProjectMemberShip)
class ProjectMemberShipAdmin(admin.ModelAdmin):
    list_display = ("user_admin", "project_admin", "role")
    list_filter = ("role", "project")
    search_fields = ("user__username", "project__title")

    def user_admin(self, obj):
        return obj.user

    user_admin.short_description = "Пользователь"

    def project_admin(self, obj):
        return obj.project.title

    project_admin.short_description = "Проект"


@admin.register(TaskRelation)
class TaskRelationAdmin(admin.ModelAdmin):
    list_display = ("relation_type", "from_task_admin", "to_task_admin", "created_date")
    list_filter = ("relation_type",)
    search_fields = ("from_task__title", "to_task__title")

    def from_task_admin(self, obj):
        return obj.from_task.title

    from_task_admin.short_description = "Исходная задача"

    def to_task_admin(self, obj):
        return obj.to_task.title

    to_task_admin.short_description = "Связанная задача"

    def created_date(self, obj):
        return obj.from_task.date

    created_date.short_description = "Дата создания"


@admin.register(AdditionalTask)
class AdditionalTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_admin")
    search_fields = ("title", "task__title")

    def task_admin(self, obj):
        return obj.task.title

    task_admin.short_description = "Основная задача"
