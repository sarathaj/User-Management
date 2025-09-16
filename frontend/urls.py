from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    # This pattern will serve the index.html at the root URL
    path("", views.index, name="index"),
    # This explicitly handles requests to /index.html
    path("index.html", views.index, name="index-html"),
]
