from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # The 'user' field is not included here because it will be set
        # automatically from the request context in the view.
        fields = [
            "id",
            "title",
            "description",
            "attachment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
