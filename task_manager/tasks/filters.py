from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from task_manager.labels.models import Label
from .models import Task
from django.utils.translation import gettext_lazy as _
from django import forms


class TaskFilter(FilterSet):

    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))

    own_tasks = BooleanFilter(label=_('Only own tasks'),
                              widget=forms.CheckboxInput,
                              method='get_own_tasks',)

    def get_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = (
            'status',
            'executor',
        )
