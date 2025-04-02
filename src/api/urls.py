from django.urls import path

from .views import (
    BoardAddColumnView,
    BoardDetailView,
    BoardListView,
    BoardUpdateColumnView,
    ProjectAddMemberView,
    ProjectDeleteMemberView,
    ProjectDetailView,
    ProjectListView,
    TaskDetailView,
    TaskListView,
)

urlpatterns = [
    # проект
    path("api/projects/", ProjectListView.as_view()),
    path("api/projects/<int:pk>", ProjectDetailView.as_view()),
    path("api/projects/<int:pk>/members", ProjectAddMemberView.as_view()),
    path(
        "api/projects/<int:pk>/members/<int:user_pk>", ProjectDeleteMemberView.as_view()
    ),
    # доска
    path("api/boards/", BoardListView.as_view()),
    path("api/boards/<int:pk>", BoardDetailView.as_view()),
    path("api/boards/<int:pk>/columns", BoardAddColumnView.as_view()),
    path(
        "api/boards/<int:pk>/columns/<int:column_id>", BoardUpdateColumnView.as_view()
    ),
    # задачи
    path("api/tasks/", TaskListView.as_view()),
    path("api/tasks/<int:pk>", TaskDetailView.as_view()),
]
