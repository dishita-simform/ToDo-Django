from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Model representing a Task assigned to a specific user.
    Each task has a title, description, status (completed or not), and timestamps.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  # Stores completion date

    class Meta:
        ordering = ['-created_at']  # Show latest tasks first

    def __str__(self):
        return f"{self.title} ({'Completed' if self.completed else 'Pending'})"