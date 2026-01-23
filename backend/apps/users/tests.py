import pytest
from datetime import timedelta
from apps.users.models import User, LearningProfile, DailyActivity
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
class TestXPService:
    """
    Tests for the XPService with CEFR multipliers.
    """
    
    def test_get_cefr_multiplier_a1(self):
        """Test A1 multiplier is 1.0."""
        from apps.users.services.xp_service import XPService
        assert XPService.get_cefr_multiplier('A1') == 1.0
    
    def test_get_cefr_multiplier_b2(self):
        """Test B2 multiplier is 2.0."""
        from apps.users.services.xp_service import XPService
        assert XPService.get_cefr_multiplier('B2') == 2.0
    
    def test_get_cefr_multiplier_c2(self):
        """Test C2 multiplier is 3.0."""
        from apps.users.services.xp_service import XPService
        assert XPService.get_cefr_multiplier('C2') == 3.0
    
    def test_get_cefr_multiplier_case_insensitive(self):
        """Test multiplier lookup is case-insensitive."""
        from apps.users.services.xp_service import XPService
        assert XPService.get_cefr_multiplier('b1') == 1.5
    
    def test_calculate_xp_word_learned_a1(self):
        """Test word_learned XP at A1 level."""
        from apps.users.services.xp_service import XPService
        xp = XPService.calculate_xp('word_learned', 'A1')
        assert xp == 10  # base 10 * 1.0
    
    def test_calculate_xp_word_learned_c2(self):
        """Test word_learned XP at C2 level."""
        from apps.users.services.xp_service import XPService
        xp = XPService.calculate_xp('word_learned', 'C2')
        assert xp == 30  # base 10 * 3.0
    
    def test_calculate_xp_exercise_with_score_bonus(self):
        """Test exercise XP includes score bonus."""
        from apps.users.services.xp_service import XPService
        # Base 10 + (score * 0.4) * multiplier
        # score=100: base 10 + 40 = 50, * 1.0 = 50
        xp = XPService.calculate_xp('exercise_complete', 'A1', score=100)
        assert xp == 50
        
        # score=0: base 10 + 0 = 10
        xp_zero = XPService.calculate_xp('exercise_complete', 'A1', score=0)
        assert xp_zero == 10
    
    def test_calculate_xp_exercise_with_cefr_multiplier(self):
        """Test exercise XP scales with CEFR level."""
        from apps.users.services.xp_service import XPService
        # A1: (10 + 40) * 1.0 = 50
        xp_a1 = XPService.calculate_xp('exercise_complete', 'A1', score=100)
        # B2: (10 + 40) * 2.0 = 100
        xp_b2 = XPService.calculate_xp('exercise_complete', 'B2', score=100)
        
        assert xp_b2 == xp_a1 * 2
    
    def test_award_exercise_xp_integration(self, user, profile):
        """Test awarding exercise XP updates profile."""
        from apps.users.services.xp_service import XPService
        
        initial_xp = profile.total_xp
        result = XPService.award_exercise_xp(user, score=80, cefr_level='A1')
        
        profile.refresh_from_db()
        # base 10 + (80 * 0.4) = 10 + 32 = 42
        assert result['xp_awarded'] == 42
        assert profile.total_xp == initial_xp + 42
    
    def test_award_milestone_xp_b2(self, user, profile):
        """Test milestone completion at B2 gives double XP."""
        from apps.users.services.xp_service import XPService
        
        result = XPService.award_milestone_complete_xp(user, cefr_level='B2')
        # base 100 * 2.0 = 200
        assert result['xp_awarded'] == 200
    
    def test_daily_goal_bonus_no_multiplier(self, user, profile):
        """Test daily goal bonus doesn't use CEFR multiplier."""
        from apps.users.services.xp_service import XPService
        
        result = XPService.award_daily_goal_bonus(user)
        assert result['xp_awarded'] == 25  # Fixed bonus
    
    # ==========================================
    # Integration Tests - Full XP Flow
    # ==========================================
    
    def test_xp_accumulation_multiple_activities(self, user, profile):
        """Test that XP accumulates correctly across multiple activities."""
        from apps.users.services.xp_service import XPService
        
        # Reset to 0
        profile.total_xp = 0
        profile.save()
        
        # Exercise B1 (score=80): (10+32)*1.5 = 63
        XPService.award_exercise_xp(user, score=80, cefr_level='B1')
        profile.refresh_from_db()
        assert profile.total_xp == 63
        
        # Word learned A2: 10*1.25 = 12
        XPService.award_word_learned_xp(user, cefr_level='A2')
        profile.refresh_from_db()
        assert profile.total_xp == 75  # 63 + 12
        
        # Milestone B2: 100*2.0 = 200
        XPService.award_milestone_complete_xp(user, cefr_level='B2')
        profile.refresh_from_db()
        assert profile.total_xp == 275  # 75 + 200
        
        # Daily goal: 25 (no multiplier)
        XPService.award_daily_goal_bonus(user)
        profile.refresh_from_db()
        assert profile.total_xp == 300  # 275 + 25
    
    def test_xp_levelup_integration(self, user, profile):
        """Test that level up works correctly via XPService."""
        from apps.users.services.xp_service import XPService
        
        # Reset to 0
        profile.total_xp = 0
        profile.current_level = 1
        profile.save()
        
        # Award 1050 XP via milestones (should reach level 2)
        # 6 milestones at B2 (200 XP each) = 1200 XP
        for _ in range(6):
            XPService.award_milestone_complete_xp(user, cefr_level='B2')
        
        profile.refresh_from_db()
        assert profile.total_xp == 1200
        assert profile.current_level == 2  # 1 + (1200 // 1000) = 2


@pytest.mark.django_db
class TestInactivityPenaltyService:
    """
    Tests for the InactivityPenaltyService.
    """
    
    def test_get_penalty_day_1_no_penalty(self):
        """Day 1 without activity has grace period - no penalty."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        assert InactivityPenaltyService.get_penalty_for_days(1) == 0
    
    def test_get_penalty_day_2(self):
        """Day 2 without activity: -5 XP."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        assert InactivityPenaltyService.get_penalty_for_days(2) == 5
    
    def test_get_penalty_day_3(self):
        """Day 3 without activity: -10 XP."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        assert InactivityPenaltyService.get_penalty_for_days(3) == 10
    
    def test_get_penalty_day_4(self):
        """Day 4 without activity: -15 XP."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        assert InactivityPenaltyService.get_penalty_for_days(4) == 15
    
    def test_get_penalty_day_5_plus_max(self):
        """Day 5+ without activity: max penalty (20 XP)."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        assert InactivityPenaltyService.get_penalty_for_days(5) == 20
        assert InactivityPenaltyService.get_penalty_for_days(10) == 20
        assert InactivityPenaltyService.get_penalty_for_days(100) == 20
    
    def test_apply_penalty_subtracts_xp(self, user, profile):
        """Test that penalty correctly subtracts XP."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        
        profile.total_xp = 100
        profile.save()
        
        result = InactivityPenaltyService.apply_penalty(user, penalty_amount=15, days_inactive=4)
        
        profile.refresh_from_db()
        assert result['applied'] is True
        assert result['xp_lost'] == 15
        assert profile.total_xp == 85
    
    def test_apply_penalty_never_below_zero(self, user, profile):
        """Test that XP never goes below 0."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        
        profile.total_xp = 10
        profile.save()
        
        result = InactivityPenaltyService.apply_penalty(user, penalty_amount=50, days_inactive=5)
        
        profile.refresh_from_db()
        assert profile.total_xp == 0  # Never negative
        assert result['xp_lost'] == 10  # Only lost what was available
    
    def test_apply_penalty_level_unchanged(self, user, profile):
        """Test that level never decreases even when losing XP."""
        from apps.users.services.inactivity_penalty_service import InactivityPenaltyService
        
        profile.total_xp = 1500
        profile.current_level = 2
        profile.save()
        
        # Apply large penalty
        InactivityPenaltyService.apply_penalty(user, penalty_amount=1000, days_inactive=50)
        
        profile.refresh_from_db()
        assert profile.total_xp == 500
        assert profile.current_level == 2  # Level stays the same!


@pytest.mark.django_db
class TestStreakService:
    """
    Tests for the StreakService.
    """
    
    def test_get_min_activity_minutes(self):
        """Test default min activity is 5 minutes."""
        from apps.users.services.streak_service import StreakService
        assert StreakService.get_min_activity_minutes() == 5
    
    def test_was_active_today_no_activity(self, user):
        """Test was_active_today returns False when no activity."""
        from apps.users.services.streak_service import StreakService
        assert StreakService.was_active_today(user) is False
    
    def test_was_active_today_below_minimum(self, user):
        """Test was_active_today returns False when below minimum."""
        from apps.users.services.streak_service import StreakService
        from apps.users.models import DailyActivity
        from django.utils import timezone
        
        # Create activity with only 3 minutes (below 5 min threshold)
        DailyActivity.objects.create(
            user=user,
            date=timezone.now().date(),
            minutes_studied=3
        )
        
        assert StreakService.was_active_today(user) is False
    
    def test_was_active_today_meets_minimum(self, user):
        """Test was_active_today returns True when meets minimum."""
        from apps.users.services.streak_service import StreakService
        from apps.users.models import DailyActivity
        from django.utils import timezone
        
        DailyActivity.objects.create(
            user=user,
            date=timezone.now().date(),
            minutes_studied=5
        )
        
        assert StreakService.was_active_today(user) is True
    
    def test_update_streak_increment(self, user, profile):
        """Test streak increments when user was active yesterday."""
        from apps.users.services.streak_service import StreakService
        from apps.users.models import DailyActivity
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now().date() - timedelta(days=1)
        
        # Create activity for yesterday
        DailyActivity.objects.create(
            user=user,
            date=yesterday,
            minutes_studied=10
        )
        
        profile.streak_days = 3
        profile.save()
        
        result = StreakService.update_streak(user)
        
        profile.refresh_from_db()
        assert result['action'] == 'incremented'
        assert profile.streak_days == 4
    
    def test_update_streak_reset(self, user, profile):
        """Test streak resets when user was NOT active yesterday."""
        from apps.users.services.streak_service import StreakService
        
        profile.streak_days = 5
        profile.save()
        
        # No activity for yesterday
        result = StreakService.update_streak(user)
        
        profile.refresh_from_db()
        assert result['action'] == 'reset'
        assert profile.streak_days == 0
    
    def test_update_streak_updates_longest(self, user, profile):
        """Test longest_streak is updated when new record."""
        from apps.users.services.streak_service import StreakService
        from apps.users.models import DailyActivity
        from django.utils import timezone
        from datetime import timedelta
        
        yesterday = timezone.now().date() - timedelta(days=1)
        
        DailyActivity.objects.create(
            user=user,
            date=yesterday,
            minutes_studied=15
        )
        
        profile.streak_days = 10
        profile.longest_streak = 8
        profile.save()
        
        StreakService.update_streak(user)
        
        profile.refresh_from_db()
        assert profile.streak_days == 11
        assert profile.longest_streak == 11  # Updated!


@pytest.mark.django_db
class TestDailyActivityService:
    """
    Tests for DailyActivityService.
    """
    
    def test_record_activity_creates_daily_activity(self, user, profile):
        """Test that recording activity creates DailyActivity for today."""
        from apps.users.services.daily_activity_service import DailyActivityService
        from apps.users.models import DailyActivity
        from django.utils import timezone
        
        result = DailyActivityService.record_activity(user, minutes=5)
        
        assert result['minutes_studied'] == 5
        assert DailyActivity.objects.filter(user=user, date=timezone.now().date()).exists()
    
    def test_record_activity_accumulates(self, user, profile):
        """Test that multiple recordings accumulate."""
        from apps.users.services.daily_activity_service import DailyActivityService
        
        DailyActivityService.record_activity(user, minutes=5)
        result = DailyActivityService.record_activity(user, minutes=7)
        
        assert result['minutes_studied'] == 12
    
    def test_record_activity_triggers_goal_met(self, user, profile):
        """Test that goal completion is detected."""
        from apps.users.services.daily_activity_service import DailyActivityService
        
        profile.daily_goal_minutes = 10
        profile.save()
        
        # First activity - not enough
        result1 = DailyActivityService.record_activity(user, minutes=5)
        assert result1['daily_goal_met'] is False
        assert result1['just_completed_goal'] is False
        
        # Second activity - reaches goal
        result2 = DailyActivityService.record_activity(user, minutes=5)
        assert result2['daily_goal_met'] is True
        assert result2['just_completed_goal'] is True  # 🎉 Celebration flag!
    
    def test_record_activity_awards_bonus_xp(self, user, profile):
        """Test that bonus XP is awarded when goal is met."""
        from apps.users.services.daily_activity_service import DailyActivityService
        
        profile.daily_goal_minutes = 5
        profile.total_xp = 0
        profile.save()
        
        result = DailyActivityService.record_activity(user, minutes=5)
        
        profile.refresh_from_db()
        assert result['bonus_xp_awarded'] == 25  # Daily goal bonus
        assert profile.total_xp == 25
    
    def test_record_activity_bonus_only_once(self, user, profile):
        """Test that bonus is only awarded once per day."""
        from apps.users.services.daily_activity_service import DailyActivityService
        
        profile.daily_goal_minutes = 5
        profile.total_xp = 0
        profile.save()
        
        # First completion - gets bonus
        result1 = DailyActivityService.record_activity(user, minutes=5)
        assert result1['bonus_xp_awarded'] == 25
        
        # More activity same day - no extra bonus
        result2 = DailyActivityService.record_activity(user, minutes=10)
        assert result2['bonus_xp_awarded'] == 0
        assert result2['just_completed_goal'] is False  # Already completed earlier
        
        profile.refresh_from_db()
        assert profile.total_xp == 25  # Only 25, not 50
    
    def test_get_today_stats(self, user, profile):
        """Test get_today_stats returns correct data."""
        from apps.users.services.daily_activity_service import DailyActivityService
        
        profile.daily_goal_minutes = 20
        profile.save()
        
        DailyActivityService.record_activity(user, minutes=10)
        
        stats = DailyActivityService.get_today_stats(user)
        
        assert stats['minutes_studied'] == 10
        assert stats['daily_goal'] == 20
        assert stats['progress_percent'] == 50
        assert stats['minutes_remaining'] == 10


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


@pytest.mark.django_db
class TestRecordSessionAPI:
    """Tests for the RecordSessionView endpoint."""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='session_user',
            email='session@test.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def profile(self, user):
        return LearningProfile.objects.create(
            user=user,
            daily_goal_minutes=15
        )
    
    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    def test_record_session_requires_auth(self, api_client):
        """Test that unauthenticated requests are rejected."""
        url = '/api/v1/users/me/record-session/'
        response = api_client.post(url, {'minutes': 5}, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_record_session_basic(self, auth_client, user, profile):
        """Test basic session recording."""
        url = '/api/v1/users/me/record-session/'
        
        response = auth_client.post(url, {'minutes': 5}, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['minutes_studied'] == 5
        assert data['daily_goal'] == 15
        assert data['daily_goal_met'] is False
        assert data['just_completed_goal'] is False
        assert data['progress_percent'] == 33  # 5/15 = 33%
    
    def test_record_session_with_xp(self, auth_client, user, profile):
        """Test session recording with XP tracking."""
        url = '/api/v1/users/me/record-session/'
        
        response = auth_client.post(url, {
            'minutes': 10,
            'xp_earned': 50,
            'activity_type': 'exercise'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check response has profile data
        assert 'streak_days' in data
        assert 'total_xp' in data
        assert 'current_level' in data
    
    def test_record_session_accumulates(self, auth_client, user, profile):
        """Test that multiple sessions accumulate."""
        url = '/api/v1/users/me/record-session/'
        
        # First session
        auth_client.post(url, {'minutes': 5}, format='json')
        
        # Second session
        response = auth_client.post(url, {'minutes': 7}, format='json')
        data = response.json()
        
        assert data['minutes_studied'] == 12
        assert data['progress_percent'] == 80  # 12/15 = 80%
    
    def test_record_session_triggers_goal_completion(self, auth_client, user, profile):
        """Test that reaching daily goal triggers celebration flag."""
        url = '/api/v1/users/me/record-session/'
        
        # First session - not yet at goal
        response1 = auth_client.post(url, {'minutes': 10}, format='json')
        assert response1.json()['just_completed_goal'] is False
        
        # Second session - reaches goal
        response2 = auth_client.post(url, {'minutes': 5}, format='json')
        data = response2.json()
        
        assert data['daily_goal_met'] is True
        assert data['just_completed_goal'] is True
        assert data['bonus_xp_awarded'] > 0  # Should award bonus XP
    
    def test_record_session_goal_only_celebrated_once(self, auth_client, user, profile):
        """Test that goal completion celebration only happens once per day."""
        url = '/api/v1/users/me/record-session/'
        
        # First session reaches goal
        auth_client.post(url, {'minutes': 15}, format='json')
        
        # Second session after goal met
        response = auth_client.post(url, {'minutes': 5}, format='json')
        data = response.json()
        
        assert data['daily_goal_met'] is True
        assert data['just_completed_goal'] is False  # Not first time
    
    def test_record_session_validation_min_minutes(self, auth_client, user, profile):
        """Test validation - minutes must be at least 1."""
        url = '/api/v1/users/me/record-session/'
        
        response = auth_client.post(url, {'minutes': 0}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_record_session_validation_max_minutes(self, auth_client, user, profile):
        """Test validation - minutes max is 180."""
        url = '/api/v1/users/me/record-session/'
        
        response = auth_client.post(url, {'minutes': 200}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_record_session_missing_minutes(self, auth_client, user, profile):
        """Test validation - minutes is required."""
        url = '/api/v1/users/me/record-session/'
        
        response = auth_client.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestActivityHistoryAPI:
    """Tests for the ActivityHistoryView endpoint."""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='activity_user',
            email='activity@test.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def profile(self, user):
        return LearningProfile.objects.create(user=user)
    
    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    def test_activity_history_empty(self, auth_client, user, profile):
        """Test activity history with no activities."""
        url = '/api/v1/users/me/activity/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['results'] == []
        assert data['total_days'] == 30
        assert data['days_active'] == 0
        assert data['total_minutes'] == 0
        assert data['total_xp'] == 0
    
    def test_activity_history_with_data(self, auth_client, user, profile):
        """Test activity history with activities."""
        from datetime import date
        
        # Create some activities
        DailyActivity.objects.create(
            user=user, date=date.today(),
            minutes_studied=15, xp_earned=75, daily_goal_met=True
        )
        DailyActivity.objects.create(
            user=user, date=date.today() - timedelta(days=1),
            minutes_studied=20, xp_earned=100, daily_goal_met=True
        )
        
        url = '/api/v1/users/me/activity/'
        response = auth_client.get(url)
        data = response.json()
        
        assert len(data['results']) == 2
        assert data['days_active'] == 2
        assert data['total_minutes'] == 35
        assert data['total_xp'] == 175
    
    def test_activity_history_custom_days(self, auth_client, user, profile):
        """Test custom days parameter."""
        url = '/api/v1/users/me/activity/?days=7'
        response = auth_client.get(url)
        data = response.json()
        
        assert data['total_days'] == 7


@pytest.mark.django_db
class TestStreakDetailAPI:
    """Tests for the StreakDetailView endpoint."""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='streak_user',
            email='streak@test.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def profile(self, user):
        return LearningProfile.objects.create(
            user=user,
            streak_days=7,
            longest_streak=15
        )
    
    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    def test_streak_detail_basic(self, auth_client, user, profile):
        """Test basic streak detail."""
        url = '/api/v1/users/me/streaks/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['current_streak'] == 7
        assert data['longest_streak'] == 15
        assert data['streak_start_date'] is not None
        assert len(data['weekly_activity']) == 7
        assert 'is_at_risk' in data
    
    def test_streak_at_risk_no_activity_today(self, auth_client, user, profile):
        """Test streak at risk when no activity today."""
        url = '/api/v1/users/me/streaks/'
        response = auth_client.get(url)
        data = response.json()
        
        # Streak > 0 but no activity today = at risk
        assert data['is_at_risk'] is True
    
    def test_streak_safe_with_activity(self, auth_client, user, profile):
        """Test streak not at risk when have activity."""
        from datetime import date
        
        # Add today's activity
        DailyActivity.objects.create(
            user=user, date=date.today(),
            minutes_studied=10
        )
        
        url = '/api/v1/users/me/streaks/'
        response = auth_client.get(url)
        data = response.json()
        
        assert data['is_at_risk'] is False


@pytest.mark.django_db
class TestXPHistoryAPI:
    """Tests for the XPHistoryView endpoint."""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='xp_user',
            email='xp@test.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def profile(self, user):
        return LearningProfile.objects.create(
            user=user,
            total_xp=2500,
            current_level=3
        )
    
    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    def test_xp_history_basic(self, auth_client, user, profile):
        """Test basic XP history."""
        url = '/api/v1/users/me/xp-history/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['current_level'] == 3
        assert data['total_xp'] == 2500
        assert data['xp_to_next_level'] == 500  # Level 3 needs 3000, has 2500
        assert data['level_progress_percent'] == 50  # 500/1000 = 50%
        assert len(data['daily_xp']) == 7  # Default 7 days
    
    def test_xp_history_custom_days(self, auth_client, user, profile):
        """Test custom days parameter."""
        url = '/api/v1/users/me/xp-history/?days=14'
        response = auth_client.get(url)
        data = response.json()
        
        assert len(data['daily_xp']) == 14


@pytest.mark.django_db
class TestUserSettingsAPI:
    """Tests for the UserSettingsView endpoint."""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='settings_user',
            email='settings@test.com',
            password='testpass123'
        )
    
    @pytest.fixture
    def profile(self, user):
        return LearningProfile.objects.create(
            user=user,
            daily_goal_minutes=15,
            learning_goal='general'
        )
    
    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client
    
    def test_get_settings(self, auth_client, user, profile):
        """Test getting user settings."""
        url = '/api/v1/users/me/settings/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data['daily_goal_minutes'] == 15
        assert data['learning_goal'] == 'general'
        assert 'preferred_ai_provider' in data
        assert 'notifications_enabled' in data
    
    def test_update_settings(self, auth_client, user, profile):
        """Test updating user settings."""
        url = '/api/v1/users/me/settings/'
        
        response = auth_client.patch(url, {
            'daily_goal_minutes': 30,
            'learning_goal': 'work'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert 'daily_goal_minutes' in data['updated_fields']
        assert 'learning_goal' in data['updated_fields']
        
        # Verify in DB
        profile.refresh_from_db()
        assert profile.daily_goal_minutes == 30
        assert profile.learning_goal == 'work'
    
    def test_settings_validation_daily_goal_min(self, auth_client, user, profile):
        """Test daily goal minimum validation."""
        url = '/api/v1/users/me/settings/'
        
        response = auth_client.patch(url, {
            'daily_goal_minutes': 1  # Below minimum
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        profile.refresh_from_db()
        assert profile.daily_goal_minutes == 5  # Clamped to minimum
    
    def test_settings_validation_daily_goal_max(self, auth_client, user, profile):
        """Test daily goal maximum validation."""
        url = '/api/v1/users/me/settings/'
        
        response = auth_client.patch(url, {
            'daily_goal_minutes': 200  # Above maximum
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        profile.refresh_from_db()
        assert profile.daily_goal_minutes == 120  # Clamped to maximum
