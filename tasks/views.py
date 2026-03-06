from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        sort = self.request.query_params.get('sort')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if sort == 'due_date':
            queryset = queryset.order_by('due_date')
        elif sort == 'priority':
            queryset = queryset.order_by('priority')
        return queryset

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise exceptions.PermissionDenied("Sorry, no permission to this task.")
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'Pending':
            task.status = 'Completed'
            task.completed_at = timezone.now()
        else:
            task.status = 'Pending'
            task.completed_at = None
        task.save()
        return Response({'status': task.status, 'completed_at': task.completed_at})
