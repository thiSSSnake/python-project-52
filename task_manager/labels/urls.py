from django.urls import path
from .views import (LabelListView,
                    LabelCreateView,
                    LabelUpdateView,
                    LabelsDeleteView)

urlpatterns = [
    path('', LabelListView.as_view(), name='labels_detail'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelsDeleteView.as_view(), name='label_delete'),
]
