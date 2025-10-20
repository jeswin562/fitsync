from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
import os
import sqlite3
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# Load environment from .env if present (so HUGGINGFACE_* vars are available)
load_dotenv()

def get_conn():
    """
    Get a raw SQLite database connection for direct SQL queries.
    This is useful for database management and direct SQL operations.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'fitness_tracker.sqlite')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/fitness_tracker.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Make csrf_token() available in all templates
    @app.context_processor
    def inject_csrf_token():
        try:
            from flask_wtf.csrf import generate_csrf
            return dict(csrf_token=generate_csrf)
        except Exception:
            return {}

    with app.app_context():
        from . import routes
        db.create_all()
        _apply_light_migrations()
        
        # Initialize exercise and food data if they don't exist
        from .models import Exercise, Food
        if not Exercise.query.first():
            init_exercise_data()
        if not Food.query.first():
            init_food_data()
            
    return app

def _apply_light_migrations():
    """Apply simple SQLite migrations without Alembic.

    - Ensure Exercise.video_url column exists.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        # Check columns in 'exercise'
        cur.execute("PRAGMA table_info(exercise);")
        cols = [row[1].lower() for row in cur.fetchall()]  # row[1] is column name
        if 'video_url' not in cols:
            cur.execute("ALTER TABLE exercise ADD COLUMN video_url VARCHAR(255);")
            conn.commit()
            print("[migrate] Added column exercise.video_url")
        conn.close()
    except Exception as e:
        # Non-fatal: log and continue
        print(f"[migrate] Skipped lightweight migrations due to error: {e}")

def init_exercise_data():
    from .models import Exercise
    exercises = [
        # Cardio exercises
        ('Running', 'Cardio', 10.0, 'Running at moderate pace'),
        ('Cycling', 'Cardio', 8.0, 'Cycling at moderate pace'),
        ('Swimming', 'Cardio', 9.0, 'Swimming freestyle'),
        ('Jump Rope', 'Cardio', 12.0, 'Jump rope at moderate pace'),
        ('Walking', 'Cardio', 4.0, 'Walking at moderate pace'),
        
        # Strength training
        ('Push-ups', 'Strength', 6.0, 'Standard push-ups'),
        ('Squats', 'Strength', 5.0, 'Bodyweight squats'),
        ('Pull-ups', 'Strength', 8.0, 'Standard pull-ups'),
        ('Plank', 'Strength', 4.0, 'Holding plank position'),
        ('Lunges', 'Strength', 5.0, 'Walking lunges'),
        
        # Yoga
        ('Yoga', 'Flexibility', 3.0, 'Gentle yoga session'),
        ('Stretching', 'Flexibility', 2.0, 'General stretching'),
        
        # Sports
        ('Basketball', 'Sports', 8.0, 'Playing basketball'),
        ('Football', 'Sports', 9.0, 'Playing football'),
        ('Tennis', 'Sports', 7.0, 'Playing tennis'),
        ('Badminton', 'Sports', 6.0, 'Playing badminton'),
    ]
    
    for name, category, cpm, desc in exercises:
        exercise = Exercise(name=name, category=category, calories_per_minute=cpm, description=desc)
        db.session.add(exercise)
    db.session.commit()

def init_food_data():
    from .models import Food
    foods = [
        # Indian Breakfast
        ('Idli', 'Breakfast', 35, '1 piece (40g)', 'Steamed rice cake'),
        ('Dosa', 'Breakfast', 120, '1 piece (50g)', 'Rice and lentil crepe'),
        ('Puri', 'Breakfast', 150, '1 piece (25g)', 'Deep fried bread'),
        ('Paratha', 'Breakfast', 180, '1 piece (60g)', 'Stuffed flatbread'),
        ('Upma', 'Breakfast', 200, '1 cup (150g)', 'Semolina breakfast'),
        
        # Indian Main Course
        ('Rice', 'Main Course', 130, '1 cup cooked (150g)', 'White rice'),
        ('Roti', 'Main Course', 80, '1 piece (30g)', 'Whole wheat flatbread'),
        ('Dal', 'Main Course', 120, '1 cup (150g)', 'Lentil curry'),
        ('Chicken Curry', 'Main Course', 250, '1 cup (150g)', 'Chicken in gravy'),
        ('Paneer Curry', 'Main Course', 280, '1 cup (150g)', 'Cottage cheese curry'),
        ('Aloo Gobi', 'Main Course', 180, '1 cup (150g)', 'Potato cauliflower curry'),
        ('Biryani', 'Main Course', 350, '1 cup (200g)', 'Spiced rice with meat'),
        
        # Indian Snacks
        ('Samosa', 'Snacks', 250, '1 piece (60g)', 'Fried pastry with filling'),
        ('Pakora', 'Snacks', 180, '1 piece (30g)', 'Fried vegetable fritters'),
        ('Bhel Puri', 'Snacks', 200, '1 cup (100g)', 'Puffed rice snack'),
        ('Chaat', 'Snacks', 300, '1 plate (150g)', 'Mixed savory snack'),
        
        # Indian Desserts
        ('Gulab Jamun', 'Desserts', 150, '1 piece (25g)', 'Sweet milk dumpling'),
        ('Rasgulla', 'Desserts', 120, '1 piece (30g)', 'Sweet cheese ball'),
        ('Jalebi', 'Desserts', 200, '1 piece (40g)', 'Sweet pretzel'),
        ('Kheer', 'Desserts', 250, '1 cup (150g)', 'Rice pudding'),
        
        # Beverages
        ('Masala Chai', 'Beverages', 80, '1 cup (200ml)', 'Spiced tea with milk'),
        ('Lassi', 'Beverages', 120, '1 glass (250ml)', 'Yogurt drink'),
        ('Coffee', 'Beverages', 5, '1 cup (200ml)', 'Black coffee'),
        ('Milk', 'Beverages', 120, '1 glass (250ml)', 'Full fat milk'),
    ]
    
    for name, category, calories, serving, desc in foods:
        food = Food(name=name, category=category, calories_per_serving=calories, serving_size=serving, description=desc)
        db.session.add(food)
    db.session.commit() 