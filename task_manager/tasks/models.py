from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
# Create your models here.

class Task(models.Model):

    name = models.CharField(max_length=150, blank=False, unique=True)
    body = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT)
    status = models.ForeignKey(Status, related_name='status', on_delete=models.PROTECT)
    executor = models.ForeignKey(User, related_name='executor', on_delete=models.PROTECT)

    def __str__(self):
        return self.name
