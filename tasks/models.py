from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=[('Low','Low'),('Medium','Medium'),('High','High')])
    status = models.CharField(max_length=10, choices=[('Pending','Pending'),('Completed','Completed')], default='Pending')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
