"""
Management command to apply inactivity penalties to users.
Run daily via cron: python manage.py apply_inactivity_penalties
"""
from django.core.management.base import BaseCommand
from apps.users.services.inactivity_penalty_service import InactivityPenaltyService


class Command(BaseCommand):
    help = 'Apply XP penalties to users who have been inactive for 2+ days'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually applying penalties',
        )
        parser.add_argument(
            '--min-days',
            type=int,
            default=2,
            help='Minimum days of inactivity to apply penalty (default: 2)',
        )
    
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        min_days = options['min_days']
        
        self.stdout.write(
            self.style.NOTICE(f'Checking for users inactive for {min_days}+ days...')
        )
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No penalties will be applied'))
        
        # Get inactive users
        inactive_users = InactivityPenaltyService.get_inactive_users(min_days=min_days)
        
        if not inactive_users:
            self.stdout.write(self.style.SUCCESS('No inactive users found. Done!'))
            return
        
        self.stdout.write(f'Found {len(inactive_users)} inactive users')
        
        total_applied = 0
        total_xp_deducted = 0
        
        for user, days_inactive in inactive_users:
            penalty = InactivityPenaltyService.get_penalty_for_days(days_inactive)
            
            if dry_run:
                self.stdout.write(
                    f'  [DRY RUN] {user.username}: {days_inactive} days inactive, '
                    f'would lose {penalty} XP'
                )
            else:
                result = InactivityPenaltyService.apply_penalty(user, penalty, days_inactive)
                
                if result.get('applied'):
                    total_applied += 1
                    total_xp_deducted += result['xp_lost']
                    self.stdout.write(
                        f'  {user.username}: {days_inactive} days inactive, '
                        f'-{result["xp_lost"]} XP ({result["old_xp"]} → {result["new_xp"]})'
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  {user.username}: Could not apply penalty')
                    )
        
        # Summary
        self.stdout.write('')
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN complete. {len(inactive_users)} users would be penalized.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Done! Applied penalties to {total_applied} users. '
                    f'Total XP deducted: {total_xp_deducted}'
                )
            )
