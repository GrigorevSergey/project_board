from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Users
from accounts.serializers import NotificationSerializer
from config import settings

from .models import Board, Project, Task
from .serializers import (
    AdditionalTaskSerializer,
    BoardSerializer,
    ProjectSerializer,
    TaskSerializer,
)


@swagger_auto_schema(
    operation_description="Управление проектом",
    request_body=ProjectSerializer,
)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related("owner").prefetch_related("members")
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):
        project = self.get_object()
        member_id = request.data.get("member_id")

        if not member_id:
            return Response(
                {"error": "member_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        member = settings.AUTH_USER_MODEL.objects.get(id=member_id)
        if not member:
            return Response(
                {"error": "Участник не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        project.members.add(member)
        return Response(
            {"message": "Участник добавлен."}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def delete_member(self, request, pk=None):
        project = self.get_object()
        member_id = request.data.get("member_id")

        if not member_id:
            return Response(
                {"error": "member_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        member = settings.AUTH_USER_MODEL.objects.get(id=member_id)
        if not member:
            return Response(
                {"error": "Участник не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        project.members.remove(member)
        return Response(
            {"message": "Участник удален."}, status=status.HTTP_204_NO_CONTENT
        )


@swagger_auto_schema(
    operation_description="Управление доской",
    request_body=BoardSerializer,
)
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    @action(detail=True, methods=["post"], url_path="columns")
    def create_column(self, request, pk=None):
        board = self.get_object()
        column_status = request.data.get("status")

        if column_status not in dict(Board.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )

        if column_status not in board.status:
            board.status.append(column_status)
            board.save()

        return Response({"statuses": board.statuses}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    operation_description="Управление задачами",
    request_body=TaskSerializer,
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @swagger_auto_schema(
        operation_description="Создание подзадачи",
        request_body=AdditionalTaskSerializer,
    )
    @action(detail=True, methods=["post"], url_path="subtasks")
    def create_subtask(self, request, pk=None):
        task = self.get_object()
        subtask_data = request.data
        subtask_data["task"] = task.id
        subtask_serializer = AdditionalTaskSerializer(data=subtask_data)

        if subtask_serializer.is_valid():
            subtask_serializer.save()
            return Response(subtask_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Добавление исполнителя",
        request_body=None,
    )
    @action(detail=True, methods=["post"], url_path="assign")
    def add_assign(self, request, pk=None):
        task = self.get_object()
        assign_id = request.data.get("assign_id")

        if not assign_id:
            return Response(
                {"error": "assign_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        assign = settings.AUTH_USER_MODEL.objects.get(id=assign_id)

        if not assign:
            return Response(
                {"error": "Исполнитель не найден."}, status=status.HTTP_404_NOT_FOUND
            )

        task.users.add(assign)
        return Response({"message": "Исполнитель добавлен."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Перемещение задачи",
        request_body=None,
    )
    @action(detail=True, methods=["post"], url_path="move")
    def move(self, request, pk=None):
        task = self.get_object()
        update_status = request.data.get("status")
        task.board.status = update_status
        task.board.save()
        return Response({"message": "Задача перемещена."}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    operation_description="Управление уведомлениями",
    request_body=NotificationSerializer,
)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Получение настроек уведомлений пользователя",
        request_body=NotificationSerializer,
    )
    @action(detail=False, methods=["get"], url_path="settings")
    def get_settings(self, request):
        user = request.user
        serializer = NotificationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Обновление настроек уведомлений пользователя",
        request_body=NotificationSerializer,
    )
    @action(detail=False, methods=["put"], url_path="settings")
    def update_settings(self, request):
        user = request.user
        serializer = NotificationSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
