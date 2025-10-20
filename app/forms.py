from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from .models import Exercise, Food
from datetime import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[Optional()])
    height = FloatField('Height (cm)', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    activity_level = SelectField('Activity Level', choices=[('sedentary', 'Sedentary'), ('light', 'Lightly Active'), ('moderate', 'Moderately Active'), ('active', 'Active'), ('very_active', 'Very Active')], validators=[Optional()])
    goal = SelectField('Fitness Goal', choices=[('lose', 'Lose Weight'), ('maintain', 'Maintain Weight'), ('gain', 'Gain Weight')], validators=[Optional()])
    target_date = StringField('Target Date', validators=[Optional()])
    submit = SubmitField('Update Profile')

class HabitForm(FlaskForm):
    name = StringField('Habit Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    frequency = SelectField('Frequency', choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Habit')

class ExerciseLogForm(FlaskForm):
    exercise_id = SelectField('Exercise', coerce=int, validators=[DataRequired()])
    duration = FloatField('Duration (minutes)', validators=[DataRequired()])
    submit = SubmitField('Log Exercise')

class FoodLogForm(FlaskForm):
    food = SelectField('Food', coerce=int, validators=[DataRequired()])
    meal_type = SelectField('Meal Type', choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner')
    ], validators=[DataRequired()])
    servings = FloatField('Servings', validators=[DataRequired()], default=1.0)
    submit = SubmitField('Log Food')

class WaterLogForm(FlaskForm):
    amount = FloatField('Water Amount (ml)', validators=[DataRequired()])
    submit = SubmitField('Log Water')

class WorkoutForm(FlaskForm):
    name = StringField('Workout Name', validators=[DataRequired()], default='')
    notes = TextAreaField('Workout Notes', validators=[Optional()])
    submit = SubmitField('Start Workout')

class ExerciseSelectionForm(FlaskForm):
    exercise_id = SelectField('Exercise', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Exercise')

class ExerciseSetForm(FlaskForm):
    reps = IntegerField('Reps', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional()])
    duration = IntegerField('Duration (seconds)', validators=[Optional()])
    distance = FloatField('Distance (km)', validators=[Optional()])
    submit = SubmitField('Add Set') 