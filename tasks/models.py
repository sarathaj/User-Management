from django.db import models
from django.contrib.auth.models import User
import os

def task_attachment_path(instance, filename):
    """Generate file path for task attachments"""
    return f'task_attachments/{instance.user.username}/{filename}'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    attachment = models.FileField(
        upload_to=task_attachment_path, 
        blank=True, 
        null=True,
        help_text="Optional file attachment"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def delete(self, *args, **kwargs):
        """Delete file when task is deleted"""
        if self.attachment:
            if os.path.isfile(self.attachment.path):
                os.remove(self.attachment.path)
        super().delete(*args, **kwargs)