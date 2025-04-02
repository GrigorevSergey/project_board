from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)

from .models import (
    AdditionalTask,
    Board,
    Project,
    ProjectMemberShip,
    Task,
    TaskRelation,
)
from .serializers import (
    AdditionalTaskSerializer,
    BoardSerializer,
    ProjectMemberShipSerializer,
    ProjectSerializer,
    TaskRelationSerializer,
    TaskSerializer,
)


class ProjectListView(ListCreateAPIView):
    queryset = Project.objects.select_related("owner").prefetch_related("members")
    serializer_class = ProjectSerializer


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.select_related("owner").prefetch_related("members").all()
    serializer_class = ProjectSerializer


class ProjectAddMemberView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        user = serializer.validated_data["user"]
        project = self.get_object()
        project.members.add(user)


class ProjectDeleteMemberView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_destroy(self, serializer):
        user = serializer.validated_data["user"]
        project = self.get_object()
        project.members.remove(user)


class BoardListView(ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    # ?????????????


class BoardAddColumnView(CreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardUpdateColumnView(UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    # изменение колонки


class TaskListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
