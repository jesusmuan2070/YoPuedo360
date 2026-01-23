"""
Django settings for yopuedo360 project.
YoPuedo360 - Language Learning Platform with AI & Memory Palace
"""

import os
from pathlib import Path
from datetime import timedelta

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_extensions',
    
    # YoPuedo360 apps
    'apps.users',
    'apps.onboarding',
    'apps.vocabulary',
    'apps.grammar',
    'apps.scenarios',
    'apps.avatar',
    'apps.learning_path',
    'apps.ai_engine',
    'apps.recommendations',
    'apps.exercises',
    'apps.intents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yopuedo360.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yopuedo360.wsgi.application'


# Database - PostgreSQL only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'yopuedo360'),
        'USER': os.environ.get('POSTGRES_USER', 'yopuedo360_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'yopuedo360_secret_2024'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5433'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User Model
AUTH_USER_MODEL = 'users.User'


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (user uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# AI Provider Configuration
AI_PROVIDERS = {
    'openai': {
        'api_key': os.environ.get('OPENAI_API_KEY', ''),
        'default_model': 'gpt-4o',
    },
    'gemini': {
        'api_key': os.environ.get('GEMINI_API_KEY', ''),
        'default_model': 'gemini-pro',
    },
}

# Default AI provider for each task type
AI_TASK_MAPPING = {
    'text_evaluation': 'openai',
    'lesson_generation': 'openai',
    'conversation': 'openai',
    'translation': 'gemini',
    'image_description': 'gemini',
}

# Learning Configuration
LEARNING_CONFIG = {
    'default_daily_goal_minutes': 15,
    'max_review_items_per_session': 20,
    'streak_freeze_cost': 50,  # XP cost for streak freeze
    
    # XP Base Values (before CEFR multiplier)
    'xp_base': {
        'exercise_complete': 10,      # + up to 40 based on score (0-100%)
        'milestone_complete': 100,    # Completing a milestone
        'word_learned': 10,           # When SRS status = 'learned'
        'word_reviewed': 2,           # Each successful SRS review
        'grammar_learned': 10,        # New grammar unit mastered
        'daily_goal_bonus': 25,       # Bonus for meeting daily goal
        'streak_bonus_per_day': 5,    # Multiplied by streak days
    },
    
    # CEFR Multipliers - Higher levels = more XP reward
    'cefr_multipliers': {
        'A1': 1.0,
        'A2': 1.25,
        'B1': 1.5,
        'B2': 2.0,
        'C1': 2.5,
        'C2': 3.0,
    },
    
    # Inactivity Penalty (XP loss for consecutive days without activity)
    # Day 1 = no penalty (grace period)
    'inactivity_penalties': {
        2: 5,   # Day 2 without activity: -5 XP
        3: 10,  # Day 3: -10 XP
        4: 15,  # Day 4: -15 XP
        # Day 5+: max_daily_penalty
    },
    'max_daily_penalty': 20,  # Max XP lost per day after day 4
    
    # Streak Configuration
    'streak': {
        'min_activity_minutes': 5,  # Minimum minutes to count as "active day"
    },
}

# Spaced Repetition (SM-2 Algorithm) Configuration
SPACED_REPETITION = {
    'initial_ease_factor': 2.5,
    'min_ease_factor': 1.3,
    'easy_bonus': 1.3,
    'interval_modifier': 1.0,
}

