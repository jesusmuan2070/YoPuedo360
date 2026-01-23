from django.urls import path
from .views import UserMeView, UserDashboardView

urlpatterns = [
    path('me/', UserMeView.as_view(), name='user_me'),
    path('me/dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
]
