import uuid
import time
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()


class TaskModelTest(TestCase):
    """Тесты моделей"""

    def setUp(self):
        self.author = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.task_data = {
            "author": self.author,
            "name": "test task",
            "description": "test task desc",
            "status": "CRTE",
        }

    def test_create_task(self):
        """Тест проверяет корректность создания задачи"""
        task = Task.objects.create(**self.task_data)
        self.assertIsInstance(task, Task)
        self.assertEqual(task.name, "test task")
        self.assertEqual(task.status, "CRTE")
        self.assertEqual(task.author, self.author)

    def test_saving_and_retrieving_tasks(self):
        """Тест на сохранение и извлечение нескольких задач"""
        _first_task = Task.objects.create(
            author=self.author,
            name="test task1",
            description="test task desc1",
            status="CRTE",
        )

        time.sleep(1)

        _second_task = Task.objects.create(
            author=self.author,
            name="test task2",
            description="test task desc2",
            status="WORK",
        )

        saved_tasks = Task.objects.all()

        self.assertEqual(saved_tasks.count(), 2)

        first_saved_task = saved_tasks[1]
        self.assertEqual(first_saved_task.name, "test task1")
        self.assertEqual(first_saved_task.description, "test task desc1")
        self.assertEqual(first_saved_task.status, "CRTE")

        second_saved_task = saved_tasks[0]
        self.assertEqual(second_saved_task.name, "test task2")
        self.assertEqual(second_saved_task.description, "test task desc2")
        self.assertEqual(second_saved_task.status, "WORK")

    def test_task_ordering(self):
        """Тест проверяет что задачи отсортированны по полю created в порядке убывания"""
        task1 = Task.objects.create(
            author=self.author,
            name="First task",
            description="First description",
            status="CRTE",
        )

        time.sleep(1)

        task2 = Task.objects.create(
            author=self.author,
            name="Second task",
            description="Second description",
            status="WORK",
        )

        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)
        self.assertEqual(tasks[1], task1)

    def test_task_default_status(self):
        """Тест проверяет автоматическую генерацию статуса"""
        task = Task.objects.create(
            author=self.author,
            name="Task with default status",
            description="Test description",
        )
        self.assertEqual(task.status, "CRTE")

    def test_task_uuid_auto_generated(self):
        """Тест проверяет автоматическую генерацию uuid поля"""
        task = Task.objects.create(**self.task_data)
        self.assertIsNotNone(task.uuid)
        self.assertIsInstance(task.uuid, uuid.UUID)

    def test_task_timestamps_auto_generated(self):
        """Тест проверяет автоматическое создания полей created и updated"""
        task = Task.objects.create(**self.task_data)
        self.assertIsNotNone(task.created)
        self.assertIsNotNone(task.updated)


class TaskAPITest(TestCase):
    """Тесты API"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass12345"
        )
        # Обходим процедуру регистрации и принудильно авторизуем клиента как указанного пользователя
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            author=self.user,
            name="Test Task",
            description="Test Description",
            status="CRTE",
        )

    def test_get_tasks_list(self):
        """Тест получения списка всех задач"""
        url = reverse("task-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        """Тест создания новой задачи"""
        url = reverse("task-list-create")
        data = {
            "name": "New task",
            "description": "New desc",
            "status": "WORK",
            "author": self.user.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["task"]["name"], "New task")

    def test_get_task_detail(self):
        """Тест получения деталей задачи"""
        url = reverse("task-detail", kwargs={"uuid": self.task.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["task"]["name"], "Test Task")

    def test_update_task(self):
        """Тест обновления задачи по uuid"""
        url = reverse("task-detail", kwargs={"uuid": self.task.uuid})
        data = {
            "name": "Updated Task",
            "description": "Updated Description",
            "status": "DONE",
            "author": self.user.id,
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["task"]["name"], "Updated Task")

    def test_delete_task(self):
        """Тест удаления задачи"""
        url = reverse("task-detail", kwargs={"uuid": self.task.uuid})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class TaskEdgeCasesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass12345"
        )
        # Обходим процедуру регистрации и принудильно авторизуем клиента как указанного пользователя
        self.client.force_authenticate(user=self.user)

    def test_task_with_max_length_name(self):
        """Тест с максимальной длиной названия"""
        max_name = "X" * 255
        task = Task.objects.create(
            author=self.user,
            name=max_name,
            description="Test",
            status="CRTE",
        )
        self.assertEqual(task.name, max_name)

    def test_task_with_empty_description(self):
        """Тест с пустым описанием"""
        task = Task.objects.create(
            author=self.user,
            name="Test",
            description="",
            status="CRTE",
        )
        self.assertEqual(task.description, "")


class TaskPerformanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass12345"
        )
        # Обходим процедуру регистрации и принудильно авторизуем клиента как указанного пользователя
        self.client.force_authenticate(user=self.user)

    def test_task_creation_performance(self):
        """Тест производительности создания задач"""
        start_time = time.time()

        for i in range(100):
            Task.objects.create(
                author=self.user,
                name=f"Task {i}",
                description="Test",
                status="CRTE",
            )

        end_time = time.time()
        self.assertLess(end_time - start_time, 1.0)  # Меньше 1 секунды


class TaskSecurityTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass12345"
        )
        # Обходим процедуру регистрации и принудильно авторизуем клиента как указанного пользователя
        self.client.force_authenticate(user=self.user)

    def test_user_cannot_access_others_tasks(self):
        """Тест что пользователь не может видеть чужие задачи"""
        another_user = User.objects.create_user(username="hacker", password="123")

        another_task = Task.objects.create(
            author=another_user,
            name="Hacker Task",
            description="Should not be visible",
            status="CRTE",
        )

        url = reverse("task-detail", kwargs={"uuid": another_task.uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
