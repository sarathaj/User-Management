from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register TaskViewSet
router = DefaultRouter()
router.register(r'', views.TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]


#TODO: Add custom routes if needed,remove if not required
# This automatically creates the following URLs:
# GET    /api/tasks/          - List tasks
# POST   /api/tasks/          - Create task
# GET    /api/tasks/{id}/     - Retrieve task
# PUT    /api/tasks/{id}/     - Update task (full)
# PATCH  /api/tasks/{id}/     - Update task (partial)
# DELETE /api/tasks/{id}/     - Delete task
# POST   /api/tasks/{id}/duplicate/  - Duplicate task
# GET    /api/tasks/recent/   - Get recent tasks
# DELETE /api/tasks/delete_all/ - Delete all tasks