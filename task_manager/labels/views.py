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
    extra_context = {
        'title': _('Labels'),
        'button_text': _('Create label'),
    }


class LabelCreateView(AuthenticationMixin, SuccessMessageMixin, CreateView):

    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_message = _("Label successfully created")
    success_url = reverse_lazy('labels_detail')
    extra_context = {
        'title': _("Create Label"),
        'button_text': _("Create"),
    }


class LabelUpdateView(AuthenticationMixin, SuccessMessageMixin, UpdateView):

    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_message = _("Label successfully updated")
    success_url = reverse_lazy('labels_detail')
    extra_context = {
        'title': _("Update Label"),
        'button_text': _("Update")
    }


class LabelsDeleteView(AuthenticationMixin, SuccessMessageMixin, DeleteView):
    '''Delete label with a protect for deleting'''
    template_name = 'delete.html'
    model = Label
    success_url = reverse_lazy('labels_detail')
    success_message = _('Label successfully deleted')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        label = self.get_object()
        context['title'] = _('Delete')
        context['message'] = _('Are you sure that you want to delete ')
        context['button_text'] = _('Yes, delete')
        context['entity_name'] = label.__str__()
        return context
