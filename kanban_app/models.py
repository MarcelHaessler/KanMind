from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """Model representing a board, with fields for title, owner, and members."""
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    members = models.ManyToManyField(User, related_name='member_boards', blank=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    """Model representing a task within a board, with fields for status, priority, assignee, reviewer, and due date."""
    class Status(models.TextChoices):
        TODO = "to-do", "To Do"
        IN_PROGRESS = "in-progress", "In Progress"
        REVIEW = "review", "Review"
        DONE = "done", "Done"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)

    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="assigned_tasks",
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="reviewing_tasks",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks",
    )

    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model representing a comment on a task, with fields for the associated task, author, content, and creation timestamp."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Kommentar von {self.author} zu {self.task}"
