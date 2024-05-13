from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse



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


def logout_user(request):
    logout(request)
    return redirect('login')
