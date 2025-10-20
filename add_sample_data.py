"""
Script to add sample data to the Fitness Habit Tracker database
This will populate the database with realistic sample data for demonstration
"""

from app import create_app, db
from app.models import User, Habit, Exercise, Food, HabitLog, ExerciseLog, FoodLog, WaterLog
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def add_sample_data():
    """Add comprehensive sample data to the database"""
    
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ADDING SAMPLE DATA TO FITNESS HABIT TRACKER DATABASE")
        print("=" * 60)
        
        # Clear existing data (optional)
        print("\n[1] Clearing existing user data...")
        User.query.delete()
        Habit.query.delete()
        HabitLog.query.delete()
        ExerciseLog.query.delete()
        FoodLog.query.delete()
        WaterLog.query.delete()
        db.session.commit()
        print("✓ Cleared existing data")
        
        # Add sample users
        print("\n[2] Adding sample users...")
        users = [
            User(
                username='john_doe',
                email='john@example.com',
                password=generate_password_hash('password123'),
                name='John Doe',
                age=25,
                gender='Male',
                height=175.0,
                weight=70.0,
                activity_level='moderate',
                goal='lose_weight'
            ),
            User(
                username='jane_smith',
                email='jane@example.com',
                password=generate_password_hash('password123'),
                name='Jane Smith',
                age=28,
                gender='Female',
                height=165.0,
                weight=60.0,
                activity_level='active',
                goal='maintain_weight'
            ),
            User(
                username='mike_wilson',
                email='mike@example.com',
                password=generate_password_hash('password123'),
                name='Mike Wilson',
                age=32,
                gender='Male',
                height=180.0,
                weight=85.0,
                activity_level='very_active',
                goal='gain_muscle'
            ),
            User(
                username='sarah_jones',
                email='sarah@example.com',
                password=generate_password_hash('password123'),
                name='Sarah Jones',
                age=24,
                gender='Female',
                height=160.0,
                weight=55.0,
                activity_level='light',
                goal='maintain_weight'
            ),
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        print(f"✓ Added {len(users)} users")
        
        # Add habits for users
        print("\n[3] Adding habits...")
        habits_data = [
            ('Morning Meditation', 'Meditate for 10 minutes every morning', 1),
            ('Drink 8 Glasses Water', 'Stay hydrated throughout the day', 1),
            ('Evening Workout', 'Exercise for 30 minutes in the evening', 1),
            ('Healthy Breakfast', 'Eat a nutritious breakfast daily', 2),
            ('Walk 10,000 Steps', 'Track daily steps and reach 10k', 2),
            ('Read Before Bed', 'Read for 20 minutes before sleeping', 3),
            ('Gym Session', 'Complete full body workout at gym', 3),
            ('Meal Prep Sunday', 'Prepare healthy meals for the week', 4),
            ('Yoga Practice', 'Practice yoga for flexibility', 4),
            ('No Sugar Challenge', 'Avoid added sugars in diet', 2),
        ]
        
        habits = []
        for name, desc, user_id in habits_data:
            habit = Habit(name=name, description=desc, user_id=user_id)
            habits.append(habit)
            db.session.add(habit)
        db.session.commit()
        print(f"✓ Added {len(habits)} habits")
        
        # Add habit logs (completions)
        print("\n[4] Adding habit completion logs...")
        habit_logs = []
        for habit in habits:
            # Add logs for the past 10 days with random completion
            for i in range(10):
                date = datetime.now().date() - timedelta(days=i)
                completed = random.choice([True, True, False])  # 66% completion rate
                log = HabitLog(habit_id=habit.id, date=date, completed=completed)
                habit_logs.append(log)
                db.session.add(log)
        db.session.commit()
        print(f"✓ Added {len(habit_logs)} habit logs")
        
        # Add exercise logs
        print("\n[5] Adding exercise logs...")
        exercises = Exercise.query.all()
        exercise_logs = []
        
        for user in users:
            for i in range(7):  # Past 7 days
                date = datetime.now().date() - timedelta(days=i)
                # Each user does 1-3 exercises per day
                num_exercises = random.randint(1, 3)
                for _ in range(num_exercises):
                    exercise = random.choice(exercises)
                    duration = random.randint(15, 60)  # 15-60 minutes
                    calories = duration * exercise.calories_per_minute
                    log = ExerciseLog(
                        exercise_id=exercise.id,
                        duration=duration,
                        calories_burned=calories,
                        date=date,
                        user_id=user.id
                    )
                    exercise_logs.append(log)
                    db.session.add(log)
        db.session.commit()
        print(f"✓ Added {len(exercise_logs)} exercise logs")
        
        # Add food logs
        print("\n[6] Adding food logs...")
        foods = Food.query.all()
        food_logs = []
        meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
        
        for user in users:
            for i in range(7):  # Past 7 days
                date = datetime.now().date() - timedelta(days=i)
                # Each user logs 3-5 meals per day
                for meal_type in random.sample(meal_types, k=random.randint(3, 4)):
                    food = random.choice(foods)
                    servings = random.uniform(0.5, 2.0)  # 0.5 to 2 servings
                    total_calories = servings * food.calories_per_serving
                    log = FoodLog(
                        food_id=food.id,
                        meal_type=meal_type,
                        servings=round(servings, 2),
                        total_calories=round(total_calories, 2),
                        date=date,
                        user_id=user.id
                    )
                    food_logs.append(log)
                    db.session.add(log)
        db.session.commit()
        print(f"✓ Added {len(food_logs)} food logs")
        
        # Add water logs
        print("\n[7] Adding water logs...")
        water_logs = []
        
        for user in users:
            for i in range(7):  # Past 7 days
                date = datetime.now().date() - timedelta(days=i)
                # 3-8 water entries per day (each glass)
                num_glasses = random.randint(3, 8)
                for _ in range(num_glasses):
                    amount = 250.0  # 250ml per glass
                    log = WaterLog(amount=amount, date=date, user_id=user.id)
                    water_logs.append(log)
                    db.session.add(log)
        db.session.commit()
        print(f"✓ Added {len(water_logs)} water logs")
        
        print("\n" + "=" * 60)
        print("SAMPLE DATA ADDED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\nSummary:")
        print(f"  Users: {len(users)}")
        print(f"  Habits: {len(habits)}")
        print(f"  Habit Logs: {len(habit_logs)}")
        print(f"  Exercise Logs: {len(exercise_logs)}")
        print(f"  Food Logs: {len(food_logs)}")
        print(f"  Water Logs: {len(water_logs)}")
        print("\nYou can now login with:")
        print("  Username: john_doe, Password: password123")
        print("  Username: jane_smith, Password: password123")
        print("  Username: mike_wilson, Password: password123")
        print("  Username: sarah_jones, Password: password123")


if __name__ == '__main__':
    add_sample_data()
