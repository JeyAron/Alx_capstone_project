from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "status",
            "completed_at",
            "created_at"
        ]

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate_priority(self, value):
        if value not in ['Low', 'Medium', 'High']:
            raise serializers.ValidationError("Priority must be Low, Medium, or High.")
        return value
