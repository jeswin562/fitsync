"""
Comprehensive exercise database for the workout system
"""
from app import create_app, db
from app.models import Exercise

def init_workout_exercises():
    app = create_app()
    with app.app_context():
        # Clear existing exercises
        Exercise.query.delete()
        
        exercises = [
            # CHEST EXERCISES
            Exercise(name='Barbell Bench Press', category='Chest', muscle_group='Pectorals', equipment='Barbell', calories_per_minute=6.0, description='Classic compound chest exercise', instructions='Lie on bench, grip barbell slightly wider than shoulders, lower to chest, press up'),
            Exercise(name='Incline Barbell Bench Press', category='Chest', muscle_group='Upper Pectorals', equipment='Barbell', calories_per_minute=6.5, description='Targets upper chest', instructions='Set bench to 30-45 degrees, perform bench press motion'),
            Exercise(name='Decline Barbell Bench Press', category='Chest', muscle_group='Lower Pectorals', equipment='Barbell', calories_per_minute=6.0, description='Targets lower chest', instructions='Set bench to decline position, perform bench press motion'),
            Exercise(name='Dumbbell Bench Press', category='Chest', muscle_group='Pectorals', equipment='Dumbbell', calories_per_minute=5.5, description='Dumbbell variation for better range of motion', instructions='Lie on bench with dumbbells, press up and together'),
            Exercise(name='Incline Dumbbell Press', category='Chest', muscle_group='Upper Pectorals', equipment='Dumbbell', calories_per_minute=6.0, description='Upper chest focus with dumbbells', instructions='Incline bench, press dumbbells up and together'),
            Exercise(name='Dumbbell Flyes', category='Chest', muscle_group='Pectorals', equipment='Dumbbell', calories_per_minute=4.0, description='Isolation exercise for chest', instructions='Lie on bench, arc dumbbells down and up in wide motion'),
            Exercise(name='Push-ups', category='Chest', muscle_group='Pectorals', equipment='Bodyweight', calories_per_minute=7.0, description='Classic bodyweight chest exercise', instructions='Start in plank, lower chest to ground, push back up'),
            Exercise(name='Chest Dips', category='Chest', muscle_group='Lower Pectorals', equipment='Bodyweight', calories_per_minute=6.5, description='Bodyweight exercise for lower chest', instructions='Lean forward on dip bars, lower and press back up'),

            # BACK EXERCISES
            Exercise(name='Deadlift', category='Back', muscle_group='Entire Back', equipment='Barbell', calories_per_minute=8.0, description='King of all exercises, full body compound', instructions='Hip hinge movement, keep bar close to body'),
            Exercise(name='Pull-ups', category='Back', muscle_group='Latissimus Dorsi', equipment='Bodyweight', calories_per_minute=8.0, description='Upper body pulling exercise', instructions='Hang from bar, pull body up until chin over bar'),
            Exercise(name='Chin-ups', category='Back', muscle_group='Latissimus Dorsi', equipment='Bodyweight', calories_per_minute=8.0, description='Underhand grip pull-ups', instructions='Underhand grip, pull up until chin over bar'),
            Exercise(name='Barbell Rows', category='Back', muscle_group='Middle Traps, Rhomboids', equipment='Barbell', calories_per_minute=6.0, description='Compound pulling exercise', instructions='Bent over position, pull bar to lower chest'),
            Exercise(name='T-Bar Row', category='Back', muscle_group='Middle Traps, Rhomboids', equipment='T-Bar', calories_per_minute=6.0, description='Thick back development', instructions='Straddle T-bar, pull to chest with neutral grip'),
            Exercise(name='Seated Cable Row', category='Back', muscle_group='Middle Traps, Rhomboids', equipment='Cable', calories_per_minute=5.0, description='Seated rowing movement', instructions='Sit upright, pull cable to lower chest'),
            Exercise(name='Lat Pulldown', category='Back', muscle_group='Latissimus Dorsi', equipment='Cable', calories_per_minute=5.0, description='Vertical pulling movement', instructions='Wide grip, pull bar down to upper chest'),
            Exercise(name='One-Arm Dumbbell Row', category='Back', muscle_group='Latissimus Dorsi', equipment='Dumbbell', calories_per_minute=5.0, description='Unilateral back exercise', instructions='Support on bench, row dumbbell to hip'),

            # LEG EXERCISES
            Exercise(name='Barbell Squat', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Barbell', calories_per_minute=8.0, description='King of leg exercises', instructions='Bar on upper back, squat down and up'),
            Exercise(name='Front Squat', category='Legs', muscle_group='Quadriceps', equipment='Barbell', calories_per_minute=7.5, description='Quad-focused squat variation', instructions='Bar on front shoulders, squat down and up'),
            Exercise(name='Leg Press', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Machine', calories_per_minute=6.0, description='Machine-based leg exercise', instructions='Feet on platform, press weight up'),
            Exercise(name='Romanian Deadlift', category='Legs', muscle_group='Hamstrings, Glutes', equipment='Barbell', calories_per_minute=7.0, description='Hip hinge movement for posterior chain', instructions='Keep knees slightly bent, hinge at hips'),
            Exercise(name='Bulgarian Split Squat', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Bodyweight', calories_per_minute=6.5, description='Single leg squat variation', instructions='Rear foot elevated, squat down on front leg'),
            Exercise(name='Walking Lunges', category='Legs', muscle_group='Quadriceps, Glutes', equipment='Bodyweight', calories_per_minute=6.0, description='Dynamic leg exercise', instructions='Step forward into lunge, alternate legs'),
            Exercise(name='Leg Curls', category='Legs', muscle_group='Hamstrings', equipment='Machine', calories_per_minute=4.0, description='Isolated hamstring exercise', instructions='Lie/sit on machine, curl heels to glutes'),
            Exercise(name='Leg Extensions', category='Legs', muscle_group='Quadriceps', equipment='Machine', calories_per_minute=4.0, description='Isolated quad exercise', instructions='Sit on machine, extend legs straight'),
            Exercise(name='Calf Raises', category='Legs', muscle_group='Calves', equipment='Bodyweight', calories_per_minute=3.0, description='Calf muscle development', instructions='Rise up on toes, lower slowly'),

            # SHOULDER EXERCISES
            Exercise(name='Overhead Press', category='Shoulders', muscle_group='Anterior Deltoids', equipment='Barbell', calories_per_minute=6.0, description='Compound shoulder exercise', instructions='Press barbell overhead from shoulder level'),
            Exercise(name='Dumbbell Shoulder Press', category='Shoulders', muscle_group='Anterior Deltoids', equipment='Dumbbell', calories_per_minute=5.5, description='Seated or standing shoulder press', instructions='Press dumbbells overhead simultaneously'),
            Exercise(name='Lateral Raises', category='Shoulders', muscle_group='Medial Deltoids', equipment='Dumbbell', calories_per_minute=3.5, description='Side delt isolation', instructions='Raise dumbbells out to sides until parallel'),
            Exercise(name='Front Raises', category='Shoulders', muscle_group='Anterior Deltoids', equipment='Dumbbell', calories_per_minute=3.5, description='Front delt isolation', instructions='Raise dumbbell forward to shoulder height'),
            Exercise(name='Rear Delt Flyes', category='Shoulders', muscle_group='Posterior Deltoids', equipment='Dumbbell', calories_per_minute=3.5, description='Rear delt isolation', instructions='Bend over, raise dumbbells out to sides'),
            Exercise(name='Upright Rows', category='Shoulders', muscle_group='Medial Deltoids, Traps', equipment='Barbell', calories_per_minute=4.5, description='Compound shoulder and trap exercise', instructions='Pull bar up along body to chest level'),
            Exercise(name='Shrugs', category='Shoulders', muscle_group='Trapezius', equipment='Dumbbell', calories_per_minute=3.0, description='Trap isolation exercise', instructions='Lift shoulders straight up and hold'),

            # ARM EXERCISES
            Exercise(name='Barbell Curls', category='Arms', muscle_group='Biceps', equipment='Barbell', calories_per_minute=3.5, description='Classic bicep exercise', instructions='Curl barbell up to chest, lower slowly'),
            Exercise(name='Dumbbell Curls', category='Arms', muscle_group='Biceps', equipment='Dumbbell', calories_per_minute=3.5, description='Bicep isolation with dumbbells', instructions='Curl dumbbells up, can be alternating or simultaneous'),
            Exercise(name='Hammer Curls', category='Arms', muscle_group='Biceps, Forearms', equipment='Dumbbell', calories_per_minute=3.5, description='Neutral grip bicep exercise', instructions='Curl with neutral grip, like holding hammer'),
            Exercise(name='Close-Grip Bench Press', category='Arms', muscle_group='Triceps', equipment='Barbell', calories_per_minute=5.5, description='Compound tricep exercise', instructions='Narrow grip bench press, elbows close to body'),
            Exercise(name='Tricep Dips', category='Arms', muscle_group='Triceps', equipment='Bodyweight', calories_per_minute=6.0, description='Bodyweight tricep exercise', instructions='Dip down on parallel bars or bench'),
            Exercise(name='Overhead Tricep Extension', category='Arms', muscle_group='Triceps', equipment='Dumbbell', calories_per_minute=3.5, description='Tricep isolation overhead', instructions='Hold dumbbell overhead, lower behind head'),
            Exercise(name='Tricep Pushdowns', category='Arms', muscle_group='Triceps', equipment='Cable', calories_per_minute=3.5, description='Cable tricep isolation', instructions='Push cable attachment down, squeeze triceps'),

            # CORE EXERCISES
            Exercise(name='Plank', category='Core', muscle_group='Core', equipment='Bodyweight', calories_per_minute=4.0, description='Isometric core exercise', instructions='Hold body straight in push-up position'),
            Exercise(name='Crunches', category='Core', muscle_group='Abdominals', equipment='Bodyweight', calories_per_minute=4.0, description='Basic ab exercise', instructions='Lie on back, curl shoulders toward knees'),
            Exercise(name='Russian Twists', category='Core', muscle_group='Obliques', equipment='Bodyweight', calories_per_minute=5.0, description='Rotational core exercise', instructions='Sit with feet up, rotate torso side to side'),
            Exercise(name='Mountain Climbers', category='Core', muscle_group='Core', equipment='Bodyweight', calories_per_minute=8.0, description='Dynamic core exercise', instructions='Plank position, alternate bringing knees to chest'),
            Exercise(name='Leg Raises', category='Core', muscle_group='Lower Abs', equipment='Bodyweight', calories_per_minute=4.0, description='Lower ab exercise', instructions='Lie on back, raise straight legs up'),
            Exercise(name='Dead Bug', category='Core', muscle_group='Core', equipment='Bodyweight', calories_per_minute=3.0, description='Core stability exercise', instructions='Lie on back, extend opposite arm and leg'),

            # CARDIO EXERCISES
            Exercise(name='Treadmill Running', category='Cardio', muscle_group='Cardiovascular', equipment='Treadmill', calories_per_minute=10.0, description='Indoor running', instructions='Maintain steady pace, monitor heart rate'),
            Exercise(name='Cycling', category='Cardio', muscle_group='Cardiovascular', equipment='Bike', calories_per_minute=8.0, description='Stationary or outdoor cycling', instructions='Maintain consistent pedaling rhythm'),
            Exercise(name='Rowing Machine', category='Cardio', muscle_group='Full Body Cardio', equipment='Rowing Machine', calories_per_minute=9.0, description='Full body cardio exercise', instructions='Drive with legs, pull with arms, reverse motion'),
            Exercise(name='Elliptical', category='Cardio', muscle_group='Cardiovascular', equipment='Elliptical', calories_per_minute=7.0, description='Low impact cardio', instructions='Smooth elliptical motion with handles'),
            Exercise(name='Jump Rope', category='Cardio', muscle_group='Cardiovascular', equipment='Jump Rope', calories_per_minute=12.0, description='High intensity cardio', instructions='Jump over rope with light bouncing motion'),
            Exercise(name='Burpees', category='Cardio', muscle_group='Full Body', equipment='Bodyweight', calories_per_minute=10.0, description='High intensity full body exercise', instructions='Squat, jump back to plank, push-up, jump forward, jump up'),
        ]
        
        for exercise in exercises:
            db.session.add(exercise)
        
        db.session.commit()
        print(f"Added {len(exercises)} exercises to the database!")

if __name__ == '__main__':
    init_workout_exercises()
