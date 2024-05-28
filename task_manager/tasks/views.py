from django.forms import BaseModelForm
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthenticationMixin, AuthorDeleteMixin
from .models import Task
from .forms import TaskForm
from task_manager.users.models import User
from django_filters.views import FilterView
from .filters import TaskFilter
# Create your views here.


class TaskListView(AuthenticationMixin, FilterView):

    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskDetailView(AuthenticationMixin, DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'
    extra_context = {
        'title': _('Viewing a task'),
    }


class TaskCreateView(AuthenticationMixin, SuccessMessageMixin, CreateView):

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')
    template_name = 'tasks/create.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''Set author of task'''
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(AuthenticationMixin, SuccessMessageMixin, UpdateView):

    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully updated')
    template_name = 'tasks/update.html'


class TaskDeleteView(AuthenticationMixin,
                     AuthorDeleteMixin,
                     SuccessMessageMixin,
                     DeleteView):

    model = Task

    template_name = 'tasks/delete.html'
    author_message = _("You can't delete this task")
    author_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    success_url = reverse_lazy('tasks')
    extra_context = {
        'title': _('Delete Task'),
    }
