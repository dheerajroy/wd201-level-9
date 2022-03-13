from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class TaskChange(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    prev_status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    curr_status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task} -> previous status: {self.prev_status} current status: {self.curr_status}'

# class Task(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     completed = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now=True)
#     deleted = models.BooleanField(default=False)
#     user = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)

#     def __str__(self):
#         return self.title