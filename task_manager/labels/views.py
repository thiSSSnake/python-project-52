from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthenticationMixin
from task_manager.tasks.models import Task
from .models import Label
from .forms import LabelForm
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.


class LabelListView(ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(AuthenticationMixin, SuccessMessageMixin, CreateView):

    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_message = _("Label successfully created")
    success_url = reverse_lazy('labels_detail')


class LabelUpdateView(AuthenticationMixin, SuccessMessageMixin, UpdateView):

    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_message = _("Label successfully updated")
    success_url = reverse_lazy('labels_detail')


class LabelsDeleteView(AuthenticationMixin, SuccessMessageMixin, DeleteView):
    '''Delete label with a protect for deleting'''
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels_detail')
    success_message = _('Label successfully deleted')
    extra_context = {
        'title': _('Delete label'),
    }

    def post(self, request, *args, **kwargs):
        label_id = kwargs['pk']
        tasks_with_label = Task.objects.filter(labels=label_id)

        if tasks_with_label:
            messages.error(
                self.request,
                _('It is not possible to delete a label '
                  'because it is in use')
            )
            return redirect('labels_detail')
        return super().post(request, *args, **kwargs)
