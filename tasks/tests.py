from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.task1 = Task.objects.create(
            user=self.user, title="Test Task 1", description="Description 1"
        )
        self.task2 = Task.objects.create(
            user=self.user, title="Test Task 2", description="Description 2"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass123"
        )
        self.other_task = Task.objects.create(
            user=self.other_user, title="Other User Task", description="Other Desc"
        )

    def test_create_task(self):
        data = {"title": "New Task", "description": "New Description"}
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)  # 3 existing + 1 new
        self.assertEqual(Task.objects.last().user, self.user)

    def test_list_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Only user's tasks
        self.assertIn("Test Task 1", str(response.data))
        self.assertNotIn("Other User Task", str(response.data))

    def test_retrieve_task(self):
        response = self.client.get(f"/api/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Task 1")

    def test_retrieve_other_user_task_forbidden(self):
        response = self.client.get(f"/api/tasks/{self.other_task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task(self):
        data = {"title": "Updated Task 1", "description": "Updated Description 1"}
        response = self.client.patch(f"/api/tasks/{self.task1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "Updated Task 1")

    def test_delete_task(self):
        response = self.client.delete(f"/api/tasks/{self.task1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 1)


    def test_delete_all_tasks(self):
        response = self.client.delete("/api/tasks/delete-all/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 0)

    def test_search_tasks(self):
        response = self.client.get("/api/tasks/?search=Task 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertIn("Test Task 1", str(response.data))
        self.assertNotIn("Test Task 2", str(response.data))

    def test_pagination(self):
        # Assuming PAGE_SIZE is 10, and we have 2 tasks, pagination will still apply
        response = self.client.get("/api/tasks/?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 2)
