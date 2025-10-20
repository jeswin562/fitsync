# Database Management System Record - Documentation
## Fitness Habit Tracker Project

---

## 📋 PROJECT OVERVIEW

**Project Name:** Fitness Habit Tracker  
**Database Type:** SQLite  
**ORM Framework:** SQLAlchemy (Flask-SQLAlchemy)  
**Programming Language:** Python 3.13  
**Web Framework:** Flask

---

## 🗄️ DATABASE CONFIGURATION

### Database Connection Code (from `app/__init__.py`)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

# Database instance
db = SQLAlchemy()

def get_conn():
    """
    Get a raw SQLite database connection for direct SQL queries.
    This function is used for database management and direct SQL operations.
    
    Returns:
        sqlite3.Connection: Database connection object with row_factory set
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'fitness_tracker.sqlite')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def create_app():
    """
    Factory function to create and configure Flask application
    with database connection
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/fitness_tracker.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create all tables
        
    return app
```

---

## 📊 DATABASE SCHEMA

### Total Tables: 12

1. **user** - Stores user account information and profile data
2. **habit** - Tracks user-defined habits
3. **habit_log** - Records daily habit completions
4. **exercise** - Exercise database with categories and calories
5. **exercise_log** - User exercise activity records
6. **food** - Food items database with nutritional info
7. **food_log** - User meal consumption records
8. **water_log** - Daily water intake tracking
9. **workout** - Workout session information
10. **workout_exercise** - Exercises within workout sessions
11. **exercise_set** - Individual sets of exercises
12. **badge** - Achievement badges for users

---

## 📝 SAMPLE SQL QUERIES

### 1. Simple SELECT Query
```sql
SELECT id, username, email, name, age, gender, goal 
FROM user 
ORDER BY id;
```

### 2. JOIN Query - Habits with User Info
```sql
SELECT 
    h.id as habit_id,
    u.username,
    h.name as habit_name,
    h.description,
    h.created_at,
    COUNT(CASE WHEN hl.completed = 1 THEN 1 END) as completed_days,
    COUNT(hl.id) as total_tracked_days
FROM habit h
JOIN user u ON h.user_id = u.id
LEFT JOIN habit_log hl ON hl.habit_id = h.id
GROUP BY h.id, u.username, h.name, h.description, h.created_at
ORDER BY h.id;
```

### 3. Complex Aggregation Query - User Statistics
```sql
SELECT 
    u.id,
    u.username,
    u.email,
    u.name,
    COUNT(DISTINCT h.id) as total_habits,
    COUNT(DISTINCT el.id) as total_exercises,
    COUNT(DISTINCT fl.id) as total_meals_logged
FROM user u
LEFT JOIN habit h ON h.user_id = u.id
LEFT JOIN exercise_log el ON el.user_id = u.id
LEFT JOIN food_log fl ON fl.user_id = u.id
GROUP BY u.id, u.username, u.email, u.name
ORDER BY u.id;
```

---

## 🔧 HOW TO RUN THE PROJECT

### 1. Add Sample Data
```bash
python add_sample_data.py
```

### 2. View Database Tables
```bash
python view_table_data.py
```

### 3. Get Screenshot-Ready Output
```bash
python show_tables_for_screenshot.py
```

### 4. Test Database Connection
```bash
python test_db_connection.py
```

### 5. Run Flask Application
```bash
python run.py
```

---

## 👥 SAMPLE USER CREDENTIALS

| Username     | Email              | Password    | Goal            |
|--------------|--------------------|-------------|-----------------|
| john_doe     | john@example.com   | password123 | lose_weight     |
| jane_smith   | jane@example.com   | password123 | maintain_weight |
| mike_wilson  | mike@example.com   | password123 | gain_muscle     |
| sarah_jones  | sarah@example.com  | password123 | maintain_weight |

---

## 📈 DATABASE STATISTICS

- **Total Users:** 4
- **Total Habits:** 10
- **Habit Completion Logs:** 100+
- **Exercise Logs:** 58+
- **Food Logs:** 101+
- **Water Logs:** 172+
- **Exercises in Database:** 50+
- **Foods in Database:** 24+

---

## 🎯 KEY FEATURES

1. **User Authentication** - Secure password hashing with Werkzeug
2. **Habit Tracking** - Daily habit completion logging
3. **Exercise Logging** - Track workouts with calorie calculations
4. **Food Tracking** - Log meals with nutritional information
5. **Water Intake** - Monitor daily hydration
6. **Progress Analytics** - View statistics and trends
7. **Achievement Badges** - Earn rewards for consistency

---

## 📂 PROJECT FILE STRUCTURE

```
Fitness Habit Tracker/
├── app/
│   ├── __init__.py          # Database configuration and app factory
│   ├── models.py            # Database models (ORM)
│   ├── routes.py            # Application routes
│   ├── forms.py             # Web forms
│   ├── utils.py             # Utility functions
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── instance/
│   └── fitness_tracker.sqlite  # SQLite database file
├── add_sample_data.py       # Script to populate database
├── view_table_data.py       # Interactive table viewer
├── show_tables_for_screenshot.py  # Screenshot-ready output
├── test_db_connection.py    # Database connection test
├── run.py                   # Application entry point
└── requirements.txt         # Python dependencies

```

---

## 🔍 FOR DBMS RECORD SUBMISSION

### Files to Include:

1. **Database Connection Code:** `app/__init__.py` (lines 1-30)
2. **Test Script:** `test_db_connection.py`
3. **Sample Data Script:** `add_sample_data.py`
4. **Table Screenshot:** Output from `show_tables_for_screenshot.py`
5. **This Documentation:** `DBMS_RECORD_DOCUMENTATION.md`

### Screenshots to Take:

1. ✅ **Habit Tracking Data Table** - Shows JOIN query results
2. ✅ **Exercise Log Data Table** - Shows exercise tracking
3. ✅ **User Statistics Report** - Shows aggregated data
4. ✅ **Database Schema** - From `test_db_connection.py` output

---

## 📝 CONCLUSION

This Fitness Habit Tracker database demonstrates:
- ✅ Proper database connection handling
- ✅ Complex SQL queries (SELECT, JOIN, GROUP BY, aggregations)
- ✅ Normalized database design
- ✅ Data integrity with foreign keys
- ✅ Real-world application with meaningful data
- ✅ Both ORM (SQLAlchemy) and raw SQL approaches

**Database Location:** `instance/fitness_tracker.sqlite`  
**Connection Type:** SQLite file-based database  
**Total Records:** 400+ across all tables

---

**Prepared for:** Database Management System Record  
**Date:** October 16, 2025  
**Project by:** Jeswin Joshy
