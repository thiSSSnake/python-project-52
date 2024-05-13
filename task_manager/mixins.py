from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError


class AuthenticationMixin(LoginRequiredMixin):
    '''Check Authentication of current User'''

    auth_messages = _('You are not logged in! You need to log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_messages)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class AuthorizationMixin(UserPassesTestMixin):
    '''Authorization Check'''

    permission_denied_message = None
    permission_denied_url = None

    def test_func(self):
        '''Check user'''

        return self.get_object() == self.request.user

    def handle_no_permission(self):
        '''If error permission,
        we handle this error and redirect to denied url'''

        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)


class DeleteProtectMixin:
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorDeleteMixin:
    author_message = None
    author_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().author.id:
            messages.error(self.request, self.author_message)
            return redirect(self.author_url)
        return super().dispatch(request, *args, **kwargs)
