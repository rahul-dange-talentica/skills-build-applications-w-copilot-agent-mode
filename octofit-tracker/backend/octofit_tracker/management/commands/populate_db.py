from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn.client[settings.DATABASES['default']['NAME']]
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Sample users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'dc'},
        ]
        db.users.insert_many(users)

        # Sample teams
        teams = [
            {'name': 'marvel', 'members': ['ironman@marvel.com', 'cap@marvel.com']},
            {'name': 'dc', 'members': ['wonderwoman@dc.com', 'batman@dc.com']},
        ]
        db.teams.insert_many(teams)

        # Sample activities
        activities = [
            {'user': 'ironman@marvel.com', 'activity': 'run', 'distance': 5},
            {'user': 'cap@marvel.com', 'activity': 'cycle', 'distance': 10},
            {'user': 'wonderwoman@dc.com', 'activity': 'swim', 'distance': 3},
            {'user': 'batman@dc.com', 'activity': 'walk', 'distance': 2},
        ]
        db.activities.insert_many(activities)

        # Sample leaderboard
        leaderboard = [
            {'team': 'marvel', 'points': 15},
            {'team': 'dc', 'points': 10},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Sample workouts
        workouts = [
            {'user': 'ironman@marvel.com', 'workout': 'pushups', 'reps': 50},
            {'user': 'cap@marvel.com', 'workout': 'situps', 'reps': 40},
            {'user': 'wonderwoman@dc.com', 'workout': 'squats', 'reps': 60},
            {'user': 'batman@dc.com', 'workout': 'pullups', 'reps': 30},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
