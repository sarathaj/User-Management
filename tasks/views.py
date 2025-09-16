from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["title", "description"]

    def get_queryset(self):
        """
        This view should return a list of all tasks for the currently authenticated user.
        """
        return self.request.user.tasks.all().order_by("-created_at")

    def perform_create(self, serializer):
        """Associates the task with the logged-in user upon creation."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="duplicate")
    def duplicate(self, request, pk=None):
        """
        Creates a duplicate of a specific task.
        """
        original_task = self.get_object()
        new_task = Task.objects.create(
            user=original_task.user,
            title=f"{original_task.title} (Copy)",
            description=original_task.description,
            # Note: attachment is not copied for simplicity.
        )
        serializer = self.get_serializer(new_task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="recent")
    def recent(self, request):
        """
        Returns tasks created in the last 7 days for the current user.
        """
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_tasks = self.get_queryset().filter(created_at__gte=seven_days_ago)
        serializer = self.get_serializer(recent_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"], url_path="delete-all")
    def delete_all(self, request):
        """
        Deletes all tasks for the current user.
        """
        tasks_to_delete = self.get_queryset()
        count = tasks_to_delete.count()
        tasks_to_delete.delete()
        return Response(
            {"detail": f"{count} tasks were deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
