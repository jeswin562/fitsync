def calculate_bmr(weight, height, age, gender):
    if not all([weight, height, age, gender]):
        return None
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity_level):
    factors = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return bmr * factors.get(activity_level, 1.2)

def check_and_award_badges(user):
    # Example: award badge for 7-day streak
    pass  # To be implemented 

# ---------------------------------
# Exercise How-To video references
# ---------------------------------

# Map normalized exercise names to reputable how-to videos (YouTube embed URLs)
EXERCISE_VIDEO_MAP = {
    # Strength basics
    "squat": {
        "title": "How to Squat Properly",
        "embed": "https://www.youtube.com/embed/YaXPRqUwItQ"
    },
    "deadlift": {
        "title": "How to Deadlift (Conventional)",
        "embed": "https://www.youtube.com/embed/op9kVnSso6Q"
    },
    "bench press": {
        "title": "How to Bench Press",
        "embed": "https://www.youtube.com/embed/gRVjAtPip0Y"
    },
    "overhead press": {
        "title": "Overhead Press Form",
        "embed": "https://www.youtube.com/embed/qEwKCR5JCog"
    },
    "shoulder press": {
        "title": "Dumbbell Shoulder Press Form",
        "embed": "https://www.youtube.com/embed/B-aVuyhvLHU"
    },
    "barbell row": {
        "title": "Barbell Row Technique",
        "embed": "https://www.youtube.com/embed/vT2GjY_Umpw"
    },
    "row": {
        "title": "Seated Cable Row Form",
        "embed": "https://www.youtube.com/embed/GZbfZ033f74"
    },
    "lat pulldown": {
        "title": "Lat Pulldown Form",
        "embed": "https://www.youtube.com/embed/CAwf7n6Luuc"
    },
    "pull up": {
        "title": "Proper Pull-Up Technique",
        "embed": "https://www.youtube.com/embed/eGo4IYlbE5g"
    },
    "pull-up": {
        "title": "Proper Pull-Up Technique",
        "embed": "https://www.youtube.com/embed/eGo4IYlbE5g"
    },
    "push up": {
        "title": "Push-Up Form Guide",
        "embed": "https://www.youtube.com/embed/IODxDxX7oi4"
    },
    "push-up": {
        "title": "Push-Up Form Guide",
        "embed": "https://www.youtube.com/embed/IODxDxX7oi4"
    },
    "lunge": {
        "title": "How to Do Lunges",
        "embed": "https://www.youtube.com/embed/QOVaHwm-Q6U"
    },
    "plank": {
        "title": "Plank Basics",
        "embed": "https://www.youtube.com/embed/pSHjTRCQxIw"
    },
    "burpee": {
        "title": "How to Do a Burpee",
        "embed": "https://www.youtube.com/embed/JZQA08SlJnM"
    },
    "bicep curl": {
        "title": "Dumbbell Bicep Curl",
        "embed": "https://www.youtube.com/embed/in7PaeYlhrM"
    },
    "tricep dip": {
        "title": "Tricep Dips",
        "embed": "https://www.youtube.com/embed/6kALZikXxLc"
    },
    "hip thrust": {
        "title": "Barbell Hip Thrust",
        "embed": "https://www.youtube.com/embed/LM8XHLYJoYs"
    },
    "romanian deadlift": {
        "title": "Romanian Deadlift (RDL)",
        "embed": "https://www.youtube.com/embed/JCXUYuzwNrM"
    },
    "incline bench": {
        "title": "Incline Bench Press",
        "embed": "https://www.youtube.com/embed/DbFgADa2PL8"
    },
    "chest fly": {
        "title": "Dumbbell Chest Fly",
        "embed": "https://www.youtube.com/embed/eozdVDA78K0"
    },
    "leg press": {
        "title": "Leg Press Machine",
        "embed": "https://www.youtube.com/embed/IZxyjW7MPJQ"
    },
}

def get_exercise_video_info(exercise_name: str):
    """Return embed URL and title for a given exercise name if known.

    Args:
        exercise_name: Name of the exercise (any case)
    Returns:
        dict with keys: title, embed; or None if not found
    """
    if not exercise_name:
        return None
    key = exercise_name.strip().lower()
    # Try exact, then some normalizations
    info = EXERCISE_VIDEO_MAP.get(key)
    if info:
        return info
    # Normalize some variants
    replacements = {
        "barbell": "",
        "dumbbell": "",
        "machine": "",
        "press": "press",
    }
    simplified = key
    for a, b in replacements.items():
        simplified = simplified.replace(a, b).strip()
    # Collapse multiple spaces
    simplified = " ".join(simplified.split())
    return EXERCISE_VIDEO_MAP.get(simplified)

def normalize_video_url(url: str) -> str:
    """Normalize a video URL into an embeddable URL (YouTube or Vimeo).

    Supports:
      YouTube:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
      Vimeo:
        - https://vimeo.com/VIDEO_ID
        - https://player.vimeo.com/video/VIDEO_ID
    """
    if not url:
        return ''
    url = url.strip()
    
    # YouTube handling
    if 'youtube.com/embed/' in url or 'youtube-nocookie.com/embed/' in url:
        return url
    if 'youtube.com/watch' in url and 'v=' in url:
        # Extract v parameter
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            vid = parse_qs(parsed.query).get('v', [''])[0]
            if vid:
                return f"https://www.youtube.com/embed/{vid}"
        except Exception:
            return url
    if 'youtu.be/' in url:
        vid = url.split('youtu.be/')[-1].split('?')[0]
        if vid:
            return f"https://www.youtube.com/embed/{vid}"
    
    # Vimeo handling
    if 'player.vimeo.com/video/' in url:
        return url  # Already in embed format
    if 'vimeo.com/' in url:
        # Extract video ID from various Vimeo URL formats
        # https://vimeo.com/123456789
        # https://vimeo.com/channels/staffpicks/123456789
        parts = url.split('vimeo.com/')[-1].split('?')[0].split('/')
        vid = parts[-1]  # Last part is always the video ID
        if vid and vid.isdigit():
            return f"https://player.vimeo.com/video/{vid}"
    
    return url
