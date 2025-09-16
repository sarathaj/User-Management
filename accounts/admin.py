from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin view for UserProfile model.
    """

    list_display = ("user", "full_name", "mobile_number", "gender", "updated_at")
    search_fields = ("user__username", "full_name", "mobile_number")
    list_filter = ("gender",)
    readonly_fields = ("created_at", "updated_at")
