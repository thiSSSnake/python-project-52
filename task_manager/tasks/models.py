from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Task(models.Model):

    name = models.CharField(max_length=150,
                            blank=False,
                            unique=True,
                            verbose_name=_('Name'))

    description = models.TextField(max_length=1000,
                                   blank=True,
                                   verbose_name=_('Description'))

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User,
                               related_name='author',
                               on_delete=models.PROTECT,
                               verbose_name=_('Author'))

    status = models.ForeignKey(Status,
                               related_name='status',
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))

    executor = models.ForeignKey(User,
                                 related_name='executor',
                                 null=True,
                                 blank=True,
                                 default='',
                                 on_delete=models.PROTECT,
                                 verbose_name=_('Executor'))

    labels = models.ManyToManyField(Label,
                                    through='TaskLabels',
                                    through_fields=('task', 'label'),
                                    blank=True,
                                    related_name='labels',
                                    verbose_name=_('Labels'))

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
