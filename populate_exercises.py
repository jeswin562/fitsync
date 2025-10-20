from app import create_app, db
from app.models import Exercise

app = create_app()
with app.app_context():
    # Clear existing exercises first
    Exercise.query.delete()
    
    exercises = [
        # CHEST EXERCISES
        Exercise(name='Barbell Bench Press', category='Chest', muscle_group='Pectorals', equipment='Barbell', calories_per_minute=6.0, description='Classic compound chest exercise', instructions='Lie on bench, grip barbell slightly wider than shoulders, lower to chest, press up'),
        Exercise(name='Incline Barbell Bench Press', category='Chest', muscle_group='Upper Pectorals', equipment='Barbell', calories_per_minute=6.5, description='Targets upper chest', instructions='Set bench to 30-45 degrees, perform bench press motion'),
        Exercise(name='Dumbbell Bench Press', category='Chest', muscle_group='Pectorals', equipment='Dumbbell', calories_per_minute=5.5, description='Dumbbell variation for better range of motion', instructions='Lie on bench with dumbbells, press up and together'),
        Exercise(name='Incline Dumbbell Press', category='Chest', muscle_group='Upper Pectorals', equipment='Dumbbell', calories_per_minute=6.0, description='Upper chest focus with dumbbells', instructions='Incline bench, press dumbbells up and together'),
        Exercise(name='Push-ups', category='Chest', muscle_group='Pectorals', equipment='Bodyweight', calories_per_minute=7.0, description='Classic bodyweight chest exercise', instructions='Start in plank, lower chest to ground, push back up'),
        Exercise(name='Chest Dips', category='Chest', muscle_group='Lower Pectorals', equipment='Bodyweight', calories_per_minute=6.5, description='Bodyweight exercise for lower chest', instructions='Lean forward on dip bars, lower and press back up'),

        # BACK EXERCISES
        Exercise(name='Deadlift', category='Back', muscle_group='Entire Back', equipment='Barbell', calories_per_minute=8.0, description='King of all exercises, full body compound', instructions='Hip hinge movement, keep bar close to body'),
        Exercise(name='Pull-ups', category='Back', muscle_group='Latissimus Dorsi', equipment='Bodyweight', calories_per_minute=8.0, description='Upper body pulling exercise', instructions='Hang from bar, pull body up until chin over bar'),
        Exercise(name='Barbell Rows', category='Back', muscle_group='Middle Traps, Rhomboids', equipment='Barbell', calories_per_minute=6.0, description='Compound pulling exercise', instructions='Bent over position, pull bar to lower chest'),
        Exercise(name='Lat Pulldown', category='Back', muscle_group='Latissimus Dorsi', equipment='Cable', calories_per_minute=5.0, description='Vertical pulling movement', instructions='Wide grip, pull bar down to upper chest'),

        # LEG EXERCISES
        Exercise(name='Barbell Squat', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Barbell', calories_per_minute=8.0, description='King of leg exercises', instructions='Bar on upper back, squat down and up'),
        Exercise(name='Leg Press', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Machine', calories_per_minute=6.0, description='Machine-based leg exercise', instructions='Feet on platform, press weight up'),
        Exercise(name='Romanian Deadlift', category='Legs', muscle_group='Hamstrings, Glutes', equipment='Barbell', calories_per_minute=7.0, description='Hip hinge movement for posterior chain', instructions='Keep knees slightly bent, hinge at hips'),
        Exercise(name='Walking Lunges', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Bodyweight', calories_per_minute=6.0, description='Dynamic leg exercise', instructions='Step forward into lunge, alternate legs'),

        # SHOULDER EXERCISES
        Exercise(name='Overhead Press', category='Shoulders', muscle_group='Anterior Deltoids', equipment='Barbell', calories_per_minute=6.0, description='Compound shoulder exercise', instructions='Press barbell overhead from shoulder level'),
        Exercise(name='Dumbbell Shoulder Press', category='Shoulders', muscle_group='Anterior Deltoids', equipment='Dumbbell', calories_per_minute=5.5, description='Seated or standing shoulder press', instructions='Press dumbbells overhead simultaneously'),
        Exercise(name='Lateral Raises', category='Shoulders', muscle_group='Medial Deltoids', equipment='Dumbbell', calories_per_minute=3.5, description='Side delt isolation', instructions='Raise dumbbells out to sides until parallel'),

        # ARM EXERCISES
        Exercise(name='Barbell Curls', category='Arms', muscle_group='Biceps', equipment='Barbell', calories_per_minute=3.5, description='Classic bicep exercise', instructions='Curl barbell up to chest, lower slowly'),
        Exercise(name='Dumbbell Curls', category='Arms', muscle_group='Biceps', equipment='Dumbbell', calories_per_minute=3.5, description='Bicep isolation with dumbbells', instructions='Curl dumbbells up, can be alternating or simultaneous'),
        Exercise(name='Tricep Dips', category='Arms', muscle_group='Triceps', equipment='Bodyweight', calories_per_minute=6.0, description='Bodyweight tricep exercise', instructions='Dip down on parallel bars or bench'),

        # CORE EXERCISES
        Exercise(name='Plank', category='Core', muscle_group='Core', equipment='Bodyweight', calories_per_minute=4.0, description='Isometric core exercise', instructions='Hold body straight in push-up position'),
        Exercise(name='Crunches', category='Core', muscle_group='Abdominals', equipment='Bodyweight', calories_per_minute=4.0, description='Basic ab exercise', instructions='Lie on back, curl shoulders toward knees'),

        # CARDIO EXERCISES
        Exercise(name='Treadmill Running', category='Cardio', muscle_group='Cardiovascular', equipment='Treadmill', calories_per_minute=10.0, description='Indoor running', instructions='Maintain steady pace, monitor heart rate'),
        Exercise(name='Cycling', category='Cardio', muscle_group='Cardiovascular', equipment='Bike', calories_per_minute=8.0, description='Stationary or outdoor cycling', instructions='Maintain consistent pedaling rhythm'),
        Exercise(name='Jump Rope', category='Cardio', muscle_group='Cardiovascular', equipment='Jump Rope', calories_per_minute=12.0, description='High intensity cardio', instructions='Jump over rope with light bouncing motion'),
    ]
    
    for exercise in exercises:
        db.session.add(exercise)
    
    db.session.commit()
    print(f"Added {len(exercises)} exercises to the database!")
    
    # Verify
    total = Exercise.query.count()
    print(f"Total exercises in database: {total}")
    
    # Show some examples
    chest_exercises = Exercise.query.filter_by(category='Chest').all()
    print(f"\nChest exercises: {len(chest_exercises)}")
    for ex in chest_exercises:
        print(f"- {ex.name}")
