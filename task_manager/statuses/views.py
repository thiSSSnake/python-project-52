from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *

# Create your views here.

class ListOfStatusesView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    extra_content = {
        'title': _('Statuses'),
    }


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    login_url = reverse_lazy('/login/')
    success_message = _('Status successfully added')
    success_url = reverse_lazy('statuses-detail')
    template_name = 'form.html'
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    login_url = reverse_lazy('/login/')
    success_message = _('Status successfully changed')
    success_url = reverse_lazy('statuses-detail')
    template_name = 'form.html'
    extra_content = {
        'title': _("Update Status"),
        'button_text': _("Update"),
    }


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    login_url = reverse_lazy('/login/')
    success_message = _('Status successfully deleted')
    success_url = reverse_lazy('statuses-detail')
    template_name = 'statuses/delete.html'
    extra_content = {
        'title': _('Delete Status'),
        'button_text': _('Delete'),
    }
