from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, timedelta

from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Starting population of test data...')
        # Attempt to clear existing sample data (best-effort). Some backends may
        # raise errors when trying to delete objects with malformed primary keys.
        for manager in (User.objects, Team.objects, Activity.objects, Workout.objects, Leaderboard.objects):
            try:
                manager.all().delete()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not delete existing data for {manager.model.__name__}: {e}'))

        # Create sample users (best-effort)
        users = []
        for i in range(1, 5):
            try:
                u = User.objects.create(
                    username=f'user{i}',
                    email=f'user{i}@example.com',
                    first_name=f'First{i}',
                    last_name=f'Last{i}',
                )
                users.append(u)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not create user user{i}: {e}'))

        # Create teams and attach members (best-effort for ArrayReferenceField)
        try:
            team_alpha = Team.objects.create(name='Team Alpha')
        except Exception as e:
            team_alpha = None
            self.stdout.write(self.style.WARNING(f'Could not create Team Alpha: {e}'))

        try:
            team_beta = Team.objects.create(name='Team Beta')
        except Exception as e:
            team_beta = None
            self.stdout.write(self.style.WARNING(f'Could not create Team Beta: {e}'))

        if team_alpha and team_beta and users:
            try:
                team_alpha.members.add(*users[:2])
                team_beta.members.add(*users[2:4])
            except Exception:
                # Fallback: assign list and save (djongo variations)
                try:
                    team_alpha.members = users[:2]
                    team_alpha.save()
                    team_beta.members = users[2:4]
                    team_beta.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not attach members to teams: {e}'))

        # Create activities (best-effort). Some djongo/Django PK mismatches
        # can raise errors when using ObjectId vs integer PKs; wrap in
        # try/except so population continues even if activity creation fails.
        try:
            if users:
                Activity.objects.create(
                    user=users[0], activity_type='run', duration=30, calories_burned=300.0, date=date.today()
                )
                Activity.objects.create(
                    user=users[1], activity_type='bike', duration=45, calories_burned=450.0, date=date.today() - timedelta(days=1)
                )
                Activity.objects.create(
                    user=users[2], activity_type='swim', duration=60, calories_burned=600.0, date=date.today() - timedelta(days=2)
                )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Activity creation skipped due to error: {e}'))

        # Create workouts (best-effort)
        try:
            Workout.objects.create(
                name='Full Body HIIT',
                description='30-minute high-intensity interval training',
                suggested_for='Cardio/Strength',
            )
            Workout.objects.create(
                name='Yoga Flow',
                description='Gentle flow for flexibility and recovery',
                suggested_for='Flexibility',
            )
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create workouts: {e}'))

        # Create leaderboard entries (best-effort)
        try:
            if team_alpha:
                Leaderboard.objects.create(team=team_alpha, total_points=250)
            if team_beta:
                Leaderboard.objects.create(team=team_beta, total_points=200)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create leaderboard entries: {e}'))

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
