import os

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="task_attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.attachment and os.path.isfile(self.attachment.path):
            os.remove(self.attachment.path)
        super().delete(*args, **kwargs)
