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

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Onboarding API (includes registration)
    path('api/v1/onboarding/', include('apps.onboarding.urls')),
    
    # Recommendations API
    path('api/v1/recommendations/', include('apps.recommendations.urls')),
    
    # Progress API
    path('api/v1/progress/', include('apps.progress.urls')),
    
    # Future: Other APIs
    # path('api/v1/users/', include('apps.users.urls')),
    # path('api/v1/content/', include('apps.content.urls')),
    # path('api/v1/worlds/', include('apps.memory_palace.urls')),
    # path('api/v1/avatar/', include('apps.avatar.urls')),
    # path('api/v1/ai/', include('apps.ai_engine.urls')),
]

