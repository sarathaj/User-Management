from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer, TaskCreateUpdateSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks with full CRUD operations
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'modified_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return tasks for the current user only"""
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a task"""
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Custom create response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        # Return full task data using the read serializer
        response_serializer = TaskSerializer(task, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Custom update response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        # Return full task data using the read serializer
        response_serializer = TaskSerializer(task, context={'request': request})
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Custom action to duplicate a task
        """
        original_task = self.get_object()
        
        # Create a duplicate
        duplicate_task = Task.objects.create(
            user=request.user,
            title=f"Copy of {original_task.title}",
            description=original_task.description,
            # Note: attachment is not duplicated for security reasons
        )
        
        serializer = TaskSerializer(duplicate_task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom action to get recent tasks (last 7 days)
        """
        from datetime import datetime, timedelta
        
        recent_date = datetime.now() - timedelta(days=7)
        recent_tasks = self.get_queryset().filter(created_at__gte=recent_date)
        
        page = self.paginate_queryset(recent_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(recent_tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """
        Custom action to delete all user's tasks
        """
        tasks_count = self.get_queryset().count()
        self.get_queryset().delete()
        
        return Response({
            'message': f'Successfully deleted {tasks_count} tasks'
        }, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        task_title = instance.title
        self.perform_destroy(instance)
        return Response({
            'message': f'Task "{task_title}" deleted successfully'
        }, status=status.HTTP_200_OK)