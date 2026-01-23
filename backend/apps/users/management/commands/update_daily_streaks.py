"""
Management command to update daily streaks for all users.
Run daily via cron: python manage.py update_daily_streaks
"""
from django.core.management.base import BaseCommand
from apps.users.services.streak_service import StreakService


class Command(BaseCommand):
    help = 'Update streak counts for all users based on yesterday activity'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually updating streaks',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.NOTICE('Processing daily streaks...')
        )
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))
            self._dry_run()
            return
        
        # Process all streaks
        results = StreakService.process_daily_streaks()
        
        # Summary
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Processed {results["processed"]} users:\n'
                f'  - Streaks incremented: {results["incremented"]}\n'
                f'  - Streaks reset: {results["reset"]}\n'
                f'  - Errors: {results["errors"]}'
            )
        )
    
    def _dry_run(self):
        """Show what would happen without making changes."""
        from apps.users.models import User
        from datetime import timedelta
        from django.utils import timezone
        
        yesterday = timezone.now().date() - timedelta(days=1)
        users = User.objects.select_related('learning_profile').all()
        
        would_increment = 0
        would_reset = 0
        
        for user in users:
            was_active = StreakService.was_active_on_date(user, yesterday)
            profile = getattr(user, 'learning_profile', None)
            
            if not profile:
                continue
            
            if was_active:
                would_increment += 1
                self.stdout.write(
                    f'  {user.username}: streak {profile.streak_days} → '
                    f'{profile.streak_days + 1} (was active)'
                )
            else:
                would_reset += 1
                self.stdout.write(
                    f'  {user.username}: streak {profile.streak_days} → 0 (inactive)'
                )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.WARNING(
                f'DRY RUN complete:\n'
                f'  - Would increment: {would_increment}\n'
                f'  - Would reset: {would_reset}'
            )
        )
