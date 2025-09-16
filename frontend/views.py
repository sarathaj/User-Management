from django.shortcuts import render


def index(request):
    """
    Renders the main index.html page for the frontend application.
    """
    return render(request, "frontend/index.html")
