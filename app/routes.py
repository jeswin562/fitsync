from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import db, login_manager, csrf
from .models import User, Habit, HabitLog, Exercise, ExerciseLog, Food, FoodLog, WaterLog, Badge, Workout, WorkoutExercise, ExerciseSet
from .forms import RegistrationForm, LoginForm, ProfileForm, HabitForm, ExerciseLogForm, FoodLogForm, WaterLogForm, WorkoutForm, ExerciseSelectionForm, ExerciseSetForm
from .utils import calculate_bmr, calculate_tdee
from .utils import get_exercise_video_info, normalize_video_url
from .models import Exercise
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from flask import Blueprint
from .mongo import get_collection, mongo_enabled  # optional MongoDB

from flask import current_app as app
from flask_login import LoginManager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensure AJAX gets JSON instead of redirect for unauthorized
@login_manager.unauthorized_handler
def unauthorized():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': False, 'error': 'unauthorized'}), 401
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find user by username first, then by email
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User.query.filter_by(email=form.username.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Only load recent data (last 7 days) for dashboard - MUCH faster
    habits = Habit.query.filter_by(user_id=current_user.id).limit(10).all()
    exercises = ExerciseLog.query.filter_by(user_id=current_user.id).filter(ExerciseLog.date >= week_ago).all()
    foods = FoodLog.query.filter_by(user_id=current_user.id).filter(FoodLog.date >= week_ago).all()
    water_logs = WaterLog.query.filter_by(user_id=current_user.id).filter(WaterLog.date >= week_ago).all()
    
    # Calculate BMR and TDEE only if user has complete profile
    bmr = None
    tdee = None
    remaining_calories = None
    if all([current_user.weight, current_user.height, current_user.age, current_user.gender, current_user.activity_level]):
        bmr = calculate_bmr(current_user.weight, current_user.height, current_user.age, current_user.gender)
        tdee = calculate_tdee(bmr, current_user.activity_level)
        
        # Calculate remaining calories for TODAY only
        foods_today = [food for food in foods if food.date == today]
        exercises_today = [ex for ex in exercises if ex.date == today]
        total_food_calories = sum(food.total_calories for food in foods_today if food.total_calories)
        total_exercise_calories = sum(ex.calories_burned for ex in exercises_today if ex.calories_burned)
        remaining_calories = tdee - total_food_calories + total_exercise_calories
    
    # Calculate total water intake for today only
    water_today = [log for log in water_logs if log.date == today]
    total_water = sum(log.amount for log in water_today)
    
    return render_template('dashboard.html', habits=habits, exercises=exercises, foods=foods, 
                         water_logs=water_logs, total_water=total_water,
                         bmr=bmr, tdee=tdee, remaining_calories=remaining_calories)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.activity_level = form.activity_level.data
        current_user.goal = form.goal.data
        if form.target_date.data:
            try:
                current_user.target_date = datetime.strptime(form.target_date.data, '%Y-%m-%d').date()
            except:
                current_user.target_date = None
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('dashboard'))
    
    # Calculate fitness stats for display
    bmr = None
    tdee = None
    target_calories = None
    bmi = None
    days_to_goal = None
    
    if all([current_user.weight, current_user.height, current_user.age, current_user.gender, current_user.activity_level]):
        bmr = calculate_bmr(current_user.weight, current_user.height, current_user.age, current_user.gender)
        tdee = calculate_tdee(bmr, current_user.activity_level)
        bmi = current_user.weight / ((current_user.height / 100) ** 2)
        
        # Calculate target calories based on goal
        if current_user.goal == 'lose':
            target_calories = tdee - 500  # 500 calorie deficit
        elif current_user.goal == 'gain':
            target_calories = tdee + 500  # 500 calorie surplus
        else:
            target_calories = tdee  # maintain
        
        # Calculate days to goal
        if current_user.target_date:
            days_to_goal = (current_user.target_date - date.today()).days
            if days_to_goal < 0:
                days_to_goal = 0
    
    return render_template('profile.html', form=form, bmr=bmr, tdee=tdee, 
                         target_calories=target_calories, bmi=bmi, days_to_goal=days_to_goal)

@app.route('/habits', methods=['GET', 'POST'])
@login_required
def habits():
    form = HabitForm()
    if form.validate_on_submit():
        habit = Habit(name=form.name.data, description=form.description.data, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
        flash('Habit added!', 'success')
        return redirect(url_for('habits'))
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template('habits.html', form=form, habits=habits)

@app.route('/habits/check/<int:habit_id>')
@login_required
def check_habit(habit_id):
    today = date.today()
    log = HabitLog.query.filter_by(habit_id=habit_id, date=today).first()
    if not log:
        log = HabitLog(habit_id=habit_id, date=today, completed=True)
        db.session.add(log)
        db.session.commit()
        flash('Habit checked for today!', 'success')
    else:
        flash('Already checked today!', 'info')
    return redirect(url_for('habits'))

@app.route('/workouts')
@login_required
def workouts():
    """Display workout history and start new workout"""
    user_workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('workouts.html', workouts=user_workouts)

@app.route('/workout/new', methods=['GET', 'POST'])
@login_required
def new_workout():
    """Start a new workout session"""
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
            name=form.name.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()

        # Mirror to MongoDB (optional)
        try:
            if mongo_enabled():
                workouts_col = get_collection("workouts")
                if workouts_col:
                    workouts_col.insert_one({
                        "sqlWorkoutId": workout.id,
                        "userId": current_user.id,
                        "name": workout.name,
                        "notes": workout.notes,
                        "date": workout.date,
                        "duration": workout.duration,
                        "exercises": []  # will be appended as exercises/sets are added
                    })
        except Exception as e:
            print(f"[Mongo] Failed to mirror new workout: {e}")

        # If a quick template was selected, pre-populate some exercises
        template = request.form.get('template', '').strip()
        if template:
            template_map = {
                'Chest Day': ['Push-ups'],
                'Back Day': ['Pull-ups'],
                'Leg Day': ['Squats', 'Lunges'],
                'Arm Day': ['Push-ups', 'Plank'],  # simple placeholders using available exercises
                'Shoulder Day': ['Stretching'],     # can replace with actual shoulder exercises if added
                'Full Body': ['Jump Rope', 'Push-ups', 'Squats', 'Plank']
            }
            names = template_map.get(template, [])
            order = 0
            for name in names:
                ex = Exercise.query.filter(Exercise.name.ilike(name)).first()
                if ex:
                    order += 1
                    we = WorkoutExercise(workout_id=workout.id, exercise_id=ex.id, order=order)
                    db.session.add(we)
            if order:
                db.session.commit()

        flash(f'Workout "{workout.name}" started!', 'success')
        return redirect(url_for('workout_session', workout_id=workout.id))
    return render_template('new_workout.html', form=form)

@app.route('/workout/<int:workout_id>')
@login_required
def workout_session(workout_id):
    """Active workout session - add exercises and sets"""
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('workouts'))
    
    # Get exercises grouped by category
    exercises_by_category = {}
    all_exercises = Exercise.query.order_by(Exercise.category, Exercise.name).all()
    for exercise in all_exercises:
        if exercise.category not in exercises_by_category:
            exercises_by_category[exercise.category] = []
        exercises_by_category[exercise.category].append(exercise)
    
    return render_template('workout_session.html', workout=workout, exercises_by_category=exercises_by_category)

@app.route('/exercise/video')
@login_required
def exercise_video_info():
    """Return embed video info for an exercise name.

    Query params:
      name: exercise name
    Response: { success: bool, title?: str, embed?: str }
    """
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({ 'success': False }), 400
    # 1) Check DB for a stored video URL (case-insensitive name match)
    ex = Exercise.query.filter(Exercise.name.ilike(name)).first()
    if ex and ex.video_url:
        return jsonify({
            'success': True,
            'title': f"How to: {ex.name}",
            'embed': normalize_video_url(ex.video_url),
            'source': 'db'
        })
    # 2) Fallback to default map
    info = get_exercise_video_info(name)
    if info:
        return jsonify({ 'success': True, **info, 'source': 'default' })
    return jsonify({ 'success': False }), 404

@app.route('/exercises/videos', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def manage_exercise_videos():
    """Simple management page to set video URLs for exercises."""
    if request.method == 'POST':
        # Expect form fields: exercise_id, video_url
        ex_id = request.form.get('exercise_id')
        vid = request.form.get('video_url', '').strip()
        if ex_id:
            ex = Exercise.query.get(int(ex_id))
            if ex:
                ex.video_url = vid or None
                db.session.commit()
                flash(f'Video updated for {ex.name}', 'success')
        return redirect(url_for('manage_exercise_videos'))

    exercises = Exercise.query.order_by(Exercise.category, Exercise.name).all()
    return render_template('manage_exercise_videos.html', exercises=exercises)

@app.route('/workout/<int:workout_id>/add_exercise', methods=['POST'])
@login_required
def add_exercise_to_workout(workout_id):
    """Add an exercise to the current workout"""
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    exercise_id = request.json.get('exercise_id')
    exercise = Exercise.query.get_or_404(exercise_id)
    
    # Check if exercise already exists in workout
    existing = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()
    if existing:
        return jsonify({'error': 'Exercise already added to workout'}), 400
    
    # Get the order for this exercise (next in sequence)
    max_order = db.session.query(db.func.max(WorkoutExercise.order)).filter_by(workout_id=workout_id).scalar() or 0
    
    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        order=max_order + 1
    )
    db.session.add(workout_exercise)
    db.session.commit()

    # Mirror exercise addition to MongoDB document
    try:
        if mongo_enabled():
            workouts_col = get_collection("workouts")
            if workouts_col:
                workouts_col.update_one(
                    {"sqlWorkoutId": workout_id, "userId": current_user.id},
                    {"$push": {"exercises": {
                        "exerciseId": exercise_id,
                        "name": exercise.name,
                        "category": exercise.category,
                        "order": max_order + 1,
                        "sets": []
                    }}}
                )
    except Exception as e:
        print(f"[Mongo] Failed to mirror add_exercise: {e}")
    
    return jsonify({
        'success': True, 
        'workout_exercise_id': workout_exercise.id,
        'exercise_name': exercise.name,
        'exercise_category': exercise.category
    })

@app.route('/workout_exercise/<int:workout_exercise_id>/add_set', methods=['POST'])
@login_required
def add_set(workout_exercise_id):
    """Add a set to an exercise in the workout"""
    workout_exercise = WorkoutExercise.query.get_or_404(workout_exercise_id)
    if workout_exercise.workout.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    
    # Get the set number (next in sequence)
    max_set = db.session.query(db.func.max(ExerciseSet.set_number)).filter_by(workout_exercise_id=workout_exercise_id).scalar() or 0
    
    exercise_set = ExerciseSet(
        workout_exercise_id=workout_exercise_id,
        set_number=max_set + 1,
        reps=data.get('reps'),
        weight=data.get('weight'),
        duration=data.get('duration'),
        distance=data.get('distance')
    )
    db.session.add(exercise_set)
    db.session.commit()

    # Mirror set addition to MongoDB document (append to last matching exercise by order)
    try:
        if mongo_enabled():
            workouts_col = get_collection("workouts")
            if workouts_col:
                we = workout_exercise
                set_doc = {
                    "setNumber": exercise_set.set_number,
                    "reps": exercise_set.reps,
                    "weight": exercise_set.weight,
                    "duration": exercise_set.duration,
                    "distance": exercise_set.distance,
                    "completed": True
                }
                # Match exercise by exerciseId and order to push set
                workouts_col.update_one(
                    {
                        "sqlWorkoutId": we.workout_id,
                        "userId": we.workout.user_id,
                        "exercises.exerciseId": we.exercise_id,
                        "exercises.order": we.order
                    },
                    {"$push": {"exercises.$.sets": set_doc}}
                )
    except Exception as e:
        print(f"[Mongo] Failed to mirror add_set: {e}")
    
    return jsonify({
        'success': True,
        'set_id': exercise_set.id,
        'set_number': exercise_set.set_number
    })

@app.route('/workout/<int:workout_id>/finish', methods=['POST'])
@login_required
def finish_workout(workout_id):
    """Complete the workout session"""
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    duration = request.json.get('duration')  # in minutes
    notes = request.json.get('notes', '')
    
    workout.duration = duration
    if notes:
        workout.notes = (workout.notes or '') + '\n' + notes
    
    db.session.commit()
    
    # Calculate some stats
    total_sets = db.session.query(ExerciseSet).join(WorkoutExercise).filter(
        WorkoutExercise.workout_id == workout_id
    ).count()
    
    total_exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).count()
    
    flash(f'Workout completed! {total_exercises} exercises, {total_sets} sets, {duration} minutes', 'success')
    return jsonify({'success': True})

# Keep the old exercise route for backward compatibility
@app.route('/exercise', methods=['GET', 'POST'])
@login_required
def exercise():
    """Legacy exercise logging - redirect to new workout system"""
    flash('Exercise logging has been upgraded! Use the new workout system for better tracking.', 'info')
    return redirect(url_for('workouts'))

@app.route('/food', methods=['GET', 'POST'])
@login_required
def food():
    form = FoodLogForm()
    
    # Get search query from request
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    # Base query
    foods_query = Food.query
    
    # Apply search filter
    if search_query:
        foods_query = foods_query.filter(
            db.or_(
                Food.name.ilike(f'%{search_query}%'),
                Food.description.ilike(f'%{search_query}%')
            )
        )
    
    # Apply category filter
    if category_filter:
        foods_query = foods_query.filter(Food.category == category_filter)
    
    # Get all foods for dropdown and filtered foods for display
    all_foods = Food.query.order_by(Food.category, Food.name).all()
    filtered_foods = foods_query.order_by(Food.category, Food.name).all()
    
    # Populate food choices for the form
    form.food.choices = [(food.id, f"{food.name} ({food.category}) - {food.calories_per_serving} cal/{food.serving_size}") for food in all_foods]
    
    if form.validate_on_submit():
        food = Food.query.get(form.food.data)
        total_calories = food.calories_per_serving * form.servings.data
        
        log = FoodLog(
            food_id=form.food.data,
            meal_type=form.meal_type.data,
            servings=form.servings.data,
            total_calories=total_calories,
            user_id=current_user.id
        )
        db.session.add(log)
        db.session.commit()
        flash(f'Food logged! {total_calories:.0f} calories consumed for {form.meal_type.data}.', 'success')
        return redirect(url_for('food'))
    
    # Only load food logs from last 30 days - much faster
    thirty_days_ago = date.today() - timedelta(days=30)
    user_foods = FoodLog.query.filter_by(user_id=current_user.id).filter(FoodLog.date >= thirty_days_ago).order_by(FoodLog.date.desc()).all()
    
    # Get unique categories for filter dropdown
    categories = db.session.query(Food.category).distinct().order_by(Food.category).all()
    categories = [cat[0] for cat in categories]
    
    return render_template('food.html', form=form, foods=user_foods, 
                         all_foods=filtered_foods, categories=categories,
                         search_query=search_query, category_filter=category_filter)

@app.route('/water', methods=['GET', 'POST'])
@login_required
def water():
    form = WaterLogForm()
    if form.validate_on_submit():
        log = WaterLog(
            amount=form.amount.data,
            user_id=current_user.id
        )
        db.session.add(log)
        db.session.commit()
        flash(f'Water logged! {form.amount.data} ml added.', 'success')
        return redirect(url_for('water'))
    
    water_logs = WaterLog.query.filter_by(user_id=current_user.id).all()
    total_water = sum(log.amount for log in water_logs if log.date == date.today())
    return render_template('water.html', form=form, water_logs=water_logs, total_water=total_water, today=date.today())


# ============================================
# AI COACH ROUTES
# ============================================

@app.route('/health/mongo')
@login_required
def mongo_health():
    """Lightweight health check for MongoDB (optional).

    Returns JSON with enabled flag and ping result if configured.
    """
    try:
        enabled = mongo_enabled()
        if not enabled:
            return jsonify({"enabled": False, "ok": False, "reason": "MONGODB_URI not configured"}), 200
        col = get_collection("__health__")
        if not col:
            return jsonify({"enabled": True, "ok": False, "reason": "DB not available"}), 200
        # Use ping command via database command
        db = col.database
        db.command("ping")
        return jsonify({"enabled": True, "ok": True}), 200
    except Exception as e:
        return jsonify({"enabled": True, "ok": False, "error": str(e)}), 200

@app.route('/ai-coach')
@login_required
def ai_coach():
    """AI Coach chat interface"""
    return render_template('ai_coach.html')


@app.route('/ai-coach/chat', methods=['POST'])
@csrf.exempt
def ai_coach_chat():
    """Handle AI coach chat messages via AJAX"""
    print("=== AI Coach Chat Route Called ===")
    
    try:
        from .ai_coach import FitnessCoach
        
        data = request.get_json()
        print(f"Received data: {data}")
        user_message = data.get('message', '').strip()
        print(f"User message: {user_message}")
        
        if not user_message:
            print("No message provided")
            return jsonify({'error': 'Message is required'}), 400
        
        # Get conversation history from session/request
        conversation_history = data.get('history', [])
        
        # Get user's recent activity data for context
        print("Getting user recent data...")
        recent_data = get_user_recent_data(current_user) if current_user.is_authenticated else {}
        print(f"Recent data: {recent_data}")
        
        # Initialize AI coach
        print("Initializing FitnessCoach...")
        coach = FitnessCoach()
        print("FitnessCoach initialized successfully")
        
        # Get AI response
        print("Getting AI response...")
        response = coach.chat(
            user_message=user_message,
            user=current_user if current_user.is_authenticated else None,
            recent_data=recent_data,
            conversation_history=conversation_history
        )
        print(f"AI Response received: {response[:100] if len(response) > 100 else response}...")
        
        result = {
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        print(f"Returning success response")
        res = make_response(jsonify(result), 200)
        res.headers['Cache-Control'] = 'no-store'
        return res
        
    except Exception as e:
        print(f"=== AI Coach Error ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        import traceback
        traceback.print_exc()
        # Return success with fallback response so user gets helpful answer
        from .ai_coach import FitnessCoach
        try:
            coach = FitnessCoach()
            safe_user = current_user if (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated) else None
            fallback = coach._get_fallback_response(user_message if 'user_message' in locals() else '', safe_user)
            res = make_response(jsonify({
                'success': True,
                'response': fallback,
                'timestamp': datetime.now().isoformat()
            }), 200)
            res.headers['Cache-Control'] = 'no-store'
            return res
        except:
            # Ultimate fallback if even that fails
            res = make_response(jsonify({
                'success': True,
                'response': "💪 I'm here to help you reach your fitness goals! Try asking me about workouts, nutrition, or motivation!",
                'timestamp': datetime.now().isoformat()
            }), 200)
            res.headers['Cache-Control'] = 'no-store'
            return res


@app.route('/ai-coach/motivation')
@login_required
def ai_coach_motivation():
    """Get daily motivation from AI coach"""
    from .ai_coach import FitnessCoach
    
    try:
        recent_data = get_user_recent_data(current_user)
        coach = FitnessCoach()
        motivation = coach.get_daily_motivation(current_user, recent_data)
        
        return jsonify({
            'success': True,
            'motivation': motivation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'motivation': "💪 You're doing great! Keep pushing towards your goals!"
        })


@app.route('/ai-coach/workout-suggestion')
@login_required
def ai_coach_workout():
    """Get workout suggestion from AI coach"""
    from .ai_coach import FitnessCoach
    
    try:
        coach = FitnessCoach()
        workout = coach.suggest_workout(current_user)
        
        return jsonify({
            'success': True,
            'workout': workout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'workout': "Try a 30-minute workout: 10 min cardio warmup, 15 min strength training, 5 min cooldown stretches!"
        })


def get_user_recent_data(user):
    """Helper function to gather user's recent activity data"""
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Get today's data
    habits_today = HabitLog.query.join(Habit).filter(
        Habit.user_id == user.id,
        HabitLog.date == today,
        HabitLog.completed == True
    ).count()
    
    exercises_today = ExerciseLog.query.filter_by(
        user_id=user.id,
        date=today
    ).all()
    
    calories_burned = sum(e.calories_burned for e in exercises_today)
    
    exercise_names = [
        f"{e.exercise.name} ({e.duration} min)"
        for e in exercises_today[:3]  # Show last 3 exercises
    ] if exercises_today else []
    
    foods_today = FoodLog.query.filter_by(
        user_id=user.id,
        date=today
    ).all()
    
    calories_consumed = sum(f.total_calories for f in foods_today)
    
    water_today = WaterLog.query.filter_by(
        user_id=user.id,
        date=today
    ).all()
    
    water_intake = sum(w.amount for w in water_today)
    
    return {
        'habits_completed': habits_today,
        'exercises': ', '.join(exercise_names) if exercise_names else 'No exercises today',
        'calories_burned': round(calories_burned, 0),
        'calories_consumed': round(calories_consumed, 0),
        'water_intake': water_intake,
    } 