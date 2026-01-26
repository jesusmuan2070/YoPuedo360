"""
Timezone utilities for user-specific date handling.

All streak and daily activity logic MUST use get_user_today() to get the correct
date in the user's timezone, not UTC.

RULE: Never compare dates using timezone.now().date() directly for streaks.
      Always use get_user_today(user).
"""
from django.utils import timezone
import pytz


def get_user_today(user):
    """
    Get today's date in the user's timezone.
    
    This is THE ONLY correct way to get "today" for streak calculations.
    Using timezone.now().date() is WRONG because it uses UTC.
    
    Args:
        user: User instance with learning_profile that has timezone field
        
    Returns:
        date object in the user's local timezone
        
    Example:
        # In Mexico at 6pm on Jan 25th:
        timezone.now().date()  # Wrong! Returns Jan 26 (UTC)
        get_user_today(user)   # Correct! Returns Jan 25 (user's time)
    """
    # Get user's timezone (default to Mexico City)
    profile = getattr(user, 'learning_profile', None)
    tz_name = profile.timezone if profile else 'America/Mexico_City'
    
    try:
        user_tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        user_tz = pytz.timezone('America/Mexico_City')
    
    # Convert current UTC time to user's timezone
    now_utc = timezone.now()
    user_now = now_utc.astimezone(user_tz)
    
    # Return only the date (not datetime)
    return user_now.date()


def get_user_yesterday(user):
    """
    Get yesterday's date in the user's timezone.
    Useful for streak continuation checks.
    """
    from datetime import timedelta
    return get_user_today(user) - timedelta(days=1)
