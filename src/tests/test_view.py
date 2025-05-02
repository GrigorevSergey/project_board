import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import Users
from api.models import Board, Project, Task


@pytest.mark.django_db
def test_project_list():
    client = APIClient()

    url = reverse("project-list")
    response = client.get(url, format="json")

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_project():
    client = APIClient()

    user = Users.objects.create_user(
        number_phone="1234567890",
        username="testuser",
        email="test@example.com",
        password="testpass",
    )

    url = reverse("project-list")
    data = {
        "title": "Test Project",
        "description": "",
        "owner": None,
        "members": [user.id],
    }
    response = client.post(url, data, format="json")

    print("Project errors:", response.data)

    assert response.status_code == 201
    assert response.data["title"] == "Test Project"
    assert Project.objects.count() == 1


@pytest.mark.django_db
def test_board_list():
    client = APIClient()

    url = reverse("board-list")
    response = client.get(url, format="json")

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_board():
    client = APIClient()

    project = Project.objects.create(title="Test Project")

    url = reverse("board-list")
    data = {
        "title": "Test Board",
        "description": "",
        "project": project.id,
        "status": "backlog",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "Test Board"
    assert Board.objects.count() == 1


@pytest.mark.django_db
def test_create_board_column():
    client = APIClient()

    project = Project.objects.create(title="Test Project")
    board = Board.objects.create(title="Test Board", project=project, status="backlog")

    url = reverse("board-create-column", kwargs={"pk": board.pk})
    data = {"status": "in_progress"}
    response = client.post(url, data, format="json")

    print("Board column errors:", response.data)

    assert response.status_code == 201
    assert response.data["status"] == "in_progress"
    assert Board.objects.get(pk=board.pk).status == "in_progress"


@pytest.mark.django_db
def test_task_list():
    client = APIClient()

    url = reverse("task-list")
    response = client.get(url, format="json")

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_task():
    client = APIClient()

    user = Users.objects.create_user(
        number_phone="1234567890",
        username="testuser",
        email="test@example.com",
        password="testpass",
    )

    project = Project.objects.create(title="Test Project")
    board = Board.objects.create(title="Test Board", project=project, status="backlog")

    url = reverse("task-list")
    data = {
        "title": "Test Task",
        "description": "",
        "board": board.id,
        "priority": "low",
        "users": [user.id],
        "date_completion": None,
        "completed_date": None,
    }
    response = client.post(url, data, format="json")

    print("Task errors:", response.data)

    assert response.status_code == 201
    assert response.data["title"] == "Test Task"
    assert Task.objects.count() == 1
