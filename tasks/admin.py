from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin view for Task model.
    """

    list_display = ("title", "user", "created_at", "updated_at")
    search_fields = ("title", "description", "user__username")
    list_filter = ("user",)
    readonly_fields = ("created_at", "updated_at")
