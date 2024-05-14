from django.urls import path
from .views import (ListOfStatusesView,
                    StatusCreateView,
                    StatusUpdateView,
                    StatusDeleteView)


urlpatterns = [
    path('', ListOfStatusesView.as_view(), name='statuses-detail'),
    path('create/', StatusCreateView.as_view(), name='statuses-create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status-update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status-delete'),
]
