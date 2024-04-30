from django.urls import path
from .views import IndexView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='users-detail'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('create/', UserCreateView.as_view(), name='users-create'),
]
