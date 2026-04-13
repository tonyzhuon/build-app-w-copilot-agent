from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        self.assertEqual(user.username, 'testuser')

class TeamModelTest(TestCase):
    def test_create_team(self):
        user = User.objects.create(username='member', email='member@example.com')
        team = Team.objects.create(name='Test Team')
        team.members.add(user)
        self.assertEqual(team.name, 'Test Team')

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        user = User.objects.create(username='activityuser', email='activity@example.com')
        activity = Activity.objects.create(user=user, activity_type='run', duration=30, calories_burned=300, date='2024-01-01')
        self.assertEqual(activity.activity_type, 'run')

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name='Pushups', description='Upper body', suggested_for='Strength')
        self.assertEqual(workout.name, 'Pushups')

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        team = Team.objects.create(name='Leaderboard Team')
        leaderboard = Leaderboard.objects.create(team=team, total_points=100)
        self.assertEqual(leaderboard.total_points, 100)


class PopulateDBCommandTest(TestCase):
    def test_populate_command_creates_expected_records(self):
        """Run the populate_db management command and verify minimum expected records."""
        from django.core.management import call_command

        # Run the management command
        call_command('populate_db')

        # After populate_db, ensure at least the sample records exist
        self.assertGreaterEqual(User.objects.count(), 4, 'Expected at least 4 users')
        self.assertGreaterEqual(Team.objects.count(), 2, 'Expected at least 2 teams')
        self.assertGreaterEqual(Workout.objects.count(), 2, 'Expected at least 2 workouts')
        self.assertGreaterEqual(Activity.objects.count(), 1, 'Expected at least 1 activity')
        self.assertGreaterEqual(Leaderboard.objects.count(), 1, 'Expected at least 1 leaderboard entry')
