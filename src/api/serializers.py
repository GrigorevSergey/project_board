from rest_framework import serializers

from .models import (
    AdditionalTask,
    Board,
    Project,
    ProjectMemberShip,
    Task,
    TaskRelation,
)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class AdditionalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalTask
        fields = "__all__"


class ProjectMemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMemberShip
        fields = "__all__"


class TaskRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRelation
        fields = "__all__"
