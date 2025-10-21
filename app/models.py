from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    activity_level = db.Column(db.String(20))
    goal = db.Column(db.String(20))
    target_date = db.Column(db.Date)
    habits = db.relationship('Habit', backref='user', lazy=True)
    exercises = db.relationship('ExerciseLog', backref='user', lazy=True)  # Old system
    workouts = db.relationship('Workout', backref='user', lazy=True)  # New system
    foods = db.relationship('FoodLog', backref='user', lazy=True)
    water_logs = db.relationship('WaterLog', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)


class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    from_user = db.relationship('User', foreign_keys=[from_user_id])
    to_user = db.relationship('User', foreign_keys=[to_user_id])

    __table_args__ = (
        db.Index('ix_friendreq_from_to', 'from_user_id', 'to_user_id'),
    )


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Store a friendship once per pair with user_a_id < user_b_id to ensure uniqueness
    user_a_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_a = db.relationship('User', foreign_keys=[user_a_id])
    user_b = db.relationship('User', foreign_keys=[user_b_id])

    __table_args__ = (
        db.UniqueConstraint('user_a_id', 'user_b_id', name='uq_friend_pair'),
        db.Index('ix_friend_pair', 'user_a_id', 'user_b_id'),
    )

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    logs = db.relationship('HabitLog', backref='habit', lazy=True)

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)  # Chest, Back, Legs, Shoulders, Arms, Core, Cardio
    muscle_group = db.Column(db.String(64))  # Primary muscle targeted
    equipment = db.Column(db.String(64))  # Barbell, Dumbbell, Machine, Bodyweight, etc.
    description = db.Column(db.String(256))
    instructions = db.Column(db.Text)  # How to perform the exercise
    calories_per_minute = db.Column(db.Float, default=5.0)  # Default for backward compatibility
    video_url = db.Column(db.String(255))  # Optional how-to video URL (YouTube embed or similar)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # e.g., "Chest Day", "Push Day"
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # Total workout duration in minutes
    notes = db.Column(db.Text)  # Workout notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class WorkoutExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    order = db.Column(db.Integer)  # Order of exercise in workout
    rest_time = db.Column(db.Integer)  # Rest time between sets in seconds
    notes = db.Column(db.Text)  # Exercise-specific notes
    
    # Relationships
    workout = db.relationship('Workout', backref='workout_exercises')
    exercise = db.relationship('Exercise', backref='workout_exercises')

class ExerciseSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_exercise_id = db.Column(db.Integer, db.ForeignKey('workout_exercise.id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)  # Weight in kg
    duration = db.Column(db.Integer)  # For time-based exercises (seconds)
    distance = db.Column(db.Float)  # For cardio exercises (km)
    completed = db.Column(db.Boolean, default=True)
    
    # Relationships
    workout_exercise = db.relationship('WorkoutExercise', backref='sets')

# Keep the old ExerciseLog for backward compatibility but mark as deprecated
class ExerciseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    duration = db.Column(db.Float)  # in minutes
    calories_burned = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise = db.relationship('Exercise', backref='logs')

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    calories_per_serving = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256))

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, snack, dinner
    servings = db.Column(db.Float, default=1.0)
    total_calories = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food = db.relationship('Food', backref='logs')

class WaterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)  # in ml
    date = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_earned = db.Column(db.Date, default=datetime.utcnow) 