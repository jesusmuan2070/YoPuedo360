"""
URL configuration for yopuedo360 project.
YoPuedo360 - Language Learning Platform API
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.serializers import CustomTokenObtainPairSerializer


# Custom login view that accepts email OR username
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # JWT Authentication (supports email or username)
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Onboarding API (includes registration)
    path('api/v1/onboarding/', include('apps.onboarding.urls')),
    
    # Recommendations API
    path('api/v1/recommendations/', include('apps.recommendations.urls')),
    
    # Progress API
    path('api/v1/progress/', include('apps.learning_path.urls')),
    
    # Intents API (Learning Orchestrator)
    path('api/v1/', include('apps.intents.urls')),
    
    # Future: Other APIs
    path('api/v1/users/', include('apps.users.urls')),
    # path('api/v1/content/', include('apps.content.urls')),
    # path('api/v1/worlds/', include('apps.memory_palace.urls')),
    # path('api/v1/avatar/', include('apps.avatar.urls')),
    # path('api/v1/ai/', include('apps.ai_engine.urls')),
]

