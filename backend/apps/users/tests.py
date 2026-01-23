import pytest
from apps.users.models import User, LearningProfile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

# ==========================================
# Shared Fixtures
# ==========================================

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def profile(user):
    # Profile is usually created by signals, but we ensure it exists or get it
    profile, _ = LearningProfile.objects.get_or_create(user=user)
    return profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_user(user, api_client):
    """Return a user and an authenticated client."""
    api_client.force_authenticate(user=user)
    return user

# ==========================================
# Tests
# ==========================================

@pytest.mark.django_db
class TestLearningProfileLogic:
    """
    Test business logic for LearningProfile model.
    Focus on XP calculation, Leveling up, and VAK style updates.
    """

    def test_initial_values(self, profile):
        """Test that a new profile starts with correct defaults."""
        assert profile.total_xp == 0
        assert profile.current_level == 1
        assert profile.primary_style == LearningProfile.LearningChannel.VISUAL

    def test_add_xp_no_levelup(self, profile):
        """Test adding XP without triggering a level up."""
        result = profile.add_xp(500)
        
        assert profile.total_xp == 500
        assert profile.current_level == 1
        assert result['leveled_up'] is False
        
        # Verify db persistence
        profile.refresh_from_db()
        assert profile.total_xp == 500

    def test_add_xp_with_levelup(self, profile):
        """Test adding XP that triggers a level up (1000 XP per level)."""
        # 1000 XP should reach level 2
        result = profile.add_xp(1050)
        
        assert profile.total_xp == 1050
        assert profile.current_level == 2
        assert result['leveled_up'] is True
        assert result['current_level'] == 2

    def test_max_level_cap(self, profile):
        """Test that level does not exceed 10."""
        # Add enough XP for level 50
        profile.add_xp(50000)
        
        assert profile.total_xp == 50000
        assert profile.current_level == 10  # Capped at 10

    def test_update_primary_style_auditory(self, profile):
        """Test that primary style updates correctly to Auditory."""
        profile.visual_score = 10
        profile.auditory_score = 90
        profile.kinesthetic_score = 20
        profile.update_primary_style()
        
        assert profile.primary_style == LearningProfile.LearningChannel.AUDITORY

    def test_update_primary_style_kinesthetic(self, profile):
        """Test that primary style updates correctly to Kinesthetic."""
        profile.visual_score = 10
        profile.auditory_score = 20
        profile.kinesthetic_score = 90
        profile.update_primary_style()
        
        assert profile.primary_style == LearningProfile.LearningChannel.KINESTHETIC

@pytest.mark.django_db
class TestUserAPI:
    """
    Integration tests for User API endpoints.
    """

    def test_get_me_unauthorized(self, api_client):
        """Test accessing /me without auth fails."""
        url = '/api/v1/users/me/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_success(self, api_client, user, profile):
        """Test accessing /me returns user and profile data."""
        # Force auth
        api_client.force_authenticate(user=user)

        url = '/api/v1/users/me/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        
        # Check User fields
        assert data['username'] == user.username
        assert data['email'] == user.email
        
        # Check Profile fields
        assert 'learning_profile' in data
        assert data['learning_profile']['current_level'] == 1
        assert data['learning_profile']['total_xp'] == 0

    def test_update_me_profile(self, api_client, auth_user, profile):
        """Test updating profile fields via /me endpoint."""
        url = '/api/v1/users/me/'
        
        payload = {
            'learning_profile': {
                'learning_goal': 'work',
                'daily_goal_minutes': 30
            }
        }
        
        response = api_client.patch(url, payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Refresh from DB
        profile.refresh_from_db()
        assert profile.learning_goal == 'work'
        assert profile.daily_goal_minutes == 30

    def test_update_me_avatar(self, api_client, auth_user):
        """Test updating user avatar via /me endpoint."""
        url = '/api/v1/users/me/'
        
        new_avatar = "https://example.com/avatar.png"
        payload = {
            'avatar_url': new_avatar
        }
        
        response = api_client.patch(url, payload, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        auth_user.refresh_from_db()
        assert auth_user.avatar_url == new_avatar

    # ==========================================
    # DELETE Account Tests
    # ==========================================

    def test_delete_me_unauthorized(self, api_client):
        """Test deleting account without auth fails."""
        url = '/api/v1/users/me/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_me_success(self, api_client, user, profile):
        """Test successful account deletion returns 204."""
        api_client.force_authenticate(user=user)
        user_id = user.id
        
        url = '/api/v1/users/me/'
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user is gone from database
        assert not User.objects.filter(id=user_id).exists()

    def test_delete_cascades_profile(self, api_client, user, profile):
        """Test that deleting user also deletes LearningProfile."""
        api_client.force_authenticate(user=user)
        profile_id = profile.id
        
        url = '/api/v1/users/me/'
        api_client.delete(url)
        
        # Verify profile is also gone
        assert not LearningProfile.objects.filter(id=profile_id).exists()


@pytest.mark.django_db
class TestUserDashboard:
    """
    Tests for the Dashboard aggregator endpoint.
    """

    def test_dashboard_unauthorized(self, api_client):
        """Test accessing dashboard without auth fails."""
        url = '/api/v1/users/me/dashboard/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dashboard_success(self, api_client, user, profile):
        """Test dashboard returns expected structure."""
        api_client.force_authenticate(user=user)
        
        url = '/api/v1/users/me/dashboard/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        
        # Check expected fields exist
        assert 'streak' in data
        assert 'current_level' in data
        assert 'total_xp' in data
        assert 'today_xp' in data
        assert 'today_minutes' in data
        assert 'daily_goal_minutes' in data
        assert 'daily_goal_met' in data
        assert 'last_7_days_xp' in data
        
        # Check last_7_days is an array of 7 items
        assert isinstance(data['last_7_days_xp'], list)
        assert len(data['last_7_days_xp']) == 7
        
        # With no activity, all should be 0
        assert data['today_xp'] == 0
        assert all(xp == 0 for xp in data['last_7_days_xp'])
