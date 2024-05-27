from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class HomePageView(TemplateView):
    '''Return Home Page'''
    template_name = "home.html"


class UserLogInView(SuccessMessageMixin, LoginView):
    '''Form log in User'''
    template_name = 'form.html'
    success_message = _('You are logged in !')


class UserLogOutView(LogoutView):
    success_message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
