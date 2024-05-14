from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


def index(request):
    '''Return Home Page'''
    return render(request, 'home.html')


class UserLogInView(SuccessMessageMixin, LoginView):
    '''Form log in User'''
    form_class = AuthenticationForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')
    success_message = _('You are logged in !')
    extra_context = {
        'title': _('Login'),
        'button_text': _('Enter'),
    }

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class UserLogOutView(LogoutView):
    next_page = reverse_lazy('home')
    success_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
