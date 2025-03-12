from django.contrib import admin

from .models import AdditionalTask, Board, Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "status")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "priority")
    list_filter = ("priority", "date")


@admin.register(AdditionalTask)
class AdditionalTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task")
