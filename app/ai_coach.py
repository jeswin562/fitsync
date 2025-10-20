"""
AI Fitness Coach using Hugging Face
Provides personalized fitness advice and motivation
"""

from huggingface_hub import InferenceClient
import os
import re
from datetime import datetime, timedelta

class FitnessCoach:
    """AI-powered fitness coach using Hugging Face"""
    
    def __init__(self, api_key=None):
        """
        Initialize the AI coach with Hugging Face API
        
        Args:
            api_key: Hugging Face API token (optional, can use free tier)
        """
        self.api_key = api_key or os.environ.get('HUGGINGFACE_API_KEY')
        # Choose model via env or default
        self.model = os.environ.get('HUGGINGFACE_MODEL', "mistralai/Mistral-7B-Instruct-v0.2")
        
        # Initialize client if we have a token (HF Inference API)
        try:
            self.client = InferenceClient(token=self.api_key) if self.api_key else None
        except Exception as e:
            print(f"Failed to initialize Hugging Face client: {e}")
            self.client = None
        
    def get_system_prompt(self):
        """System prompt to guide the AI's behavior"""
        return """You are an expert fitness coach and nutritionist. Your role is to:
- Provide personalized fitness and health advice
- Motivate users to reach their fitness goals
- Offer workout suggestions based on user data
- Give nutritional guidance
- Be encouraging, supportive, and professional
- Keep responses concise (2-3 paragraphs max)
- Use emojis occasionally to be friendly

Always consider the user's:
- Current fitness goals (lose weight, gain muscle, maintain weight)
- Activity level and recent workouts
- Dietary habits
- Personal stats (age, height, weight)

Be encouraging but realistic. Safety first!"""

    def build_user_context(self, user, recent_data=None):
        """
        Build context about the user for personalized responses
        
        Args:
            user: User object from database
            recent_data: Dict with recent activity (habits, exercises, foods, water)
        """
        context = f"""
User Profile:
- Name: {user.name or user.username}
- Age: {user.age} years old
- Gender: {user.gender}
- Height: {user.height} cm, Weight: {user.weight} kg
- Fitness Goal: {user.goal.replace('_', ' ').title() if user.goal else 'Not set'}
- Activity Level: {user.activity_level.replace('_', ' ').title() if user.activity_level else 'Not set'}
"""
        
        if recent_data:
            if recent_data.get('habits_completed'):
                context += f"\nRecent Habits: Completed {recent_data['habits_completed']} habits today"
            
            if recent_data.get('exercises'):
                context += f"\nRecent Exercise: {recent_data['exercises']}"
            
            if recent_data.get('calories_burned'):
                context += f"\nCalories Burned Today: {recent_data['calories_burned']} kcal"
            
            if recent_data.get('calories_consumed'):
                context += f"\nCalories Consumed Today: {recent_data['calories_consumed']} kcal"
            
            if recent_data.get('water_intake'):
                context += f"\nWater Intake Today: {recent_data['water_intake']} ml"
        
        return context

    def chat(self, user_message, user=None, recent_data=None, conversation_history=None):
        """
        Send a message to the AI coach and get a response
        
        Args:
            user_message: User's question or message
            user: User object (optional, for personalization)
            recent_data: Recent activity data (optional)
            conversation_history: List of previous messages (optional)
        
        Returns:
            AI coach's response as string
        """
        try:
            # Build the conversation
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Add user context if available
            if user:
                user_context = self.build_user_context(user, recent_data)
                messages.append({
                    "role": "system", 
                    "content": f"Current user information:\n{user_context}"
                })
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from Hugging Face (guarded)
            import requests
            try:
                if not self.client:
                    raise RuntimeError("HF client not initialized (no token)")
                # First try OpenAI-style chat if supported by the model/endpoint
                response = self.client.chat_completion(
                    messages=messages,
                    model=self.model,
                    max_tokens=500,
                    temperature=0.7
                )
                assistant_message = response.choices[0].message.content
                return assistant_message.strip()
            except Exception as hf_err:
                print(f"Hugging Face chat_completion failed: {hf_err}. Trying text_generation...")
                try:
                    # Flatten chat into a single prompt for models that only support text-generation
                    def to_prompt(msgs):
                        parts = []
                        role_map = {"system": "System", "user": "User", "assistant": "Assistant"}
                        for m in msgs:
                            role = role_map.get(m.get("role", "user"), "User")
                            content = m.get("content", "").strip()
                            if content:
                                parts.append(f"{role}: {content}")
                        parts.append("Assistant:")
                        return "\n".join(parts)

                    prompt = to_prompt(messages)
                    tg = self.client.text_generation(
                        prompt,
                        model=self.model,
                        max_new_tokens=500,
                        temperature=0.7,
                    )
                    if isinstance(tg, str):
                        return tg.strip()
                    # Some clients return dict-like responses
                    if isinstance(tg, dict) and tg.get("generated_text"):
                        return tg["generated_text"].strip()
                    # If response shape unexpected, fall back
                    print("Unexpected text_generation response shape; using fallback")
                    return self._get_fallback_response(user_message, user)
                except Exception as tg_err:
                    print(f"Hugging Face text_generation failed: {tg_err}. Using fallback.")
                    return self._get_fallback_response(user_message, user)
            
        except requests.exceptions.Timeout:
            print("Hugging Face API timeout - using fallback")
            return self._get_fallback_response(user_message, user)
        except requests.exceptions.ConnectionError:
            print("Hugging Face API connection error - using fallback")
            return self._get_fallback_response(user_message, user)
        except Exception as e:
            print(f"Hugging Face API error: {e} - using fallback")
            # Fallback response if API fails (works great without API key!)
            return self._get_fallback_response(user_message, user)
    
    def _get_fallback_response(self, user_message, user=None):
        """Provide a smart response if API fails"""
        
        message_lower = user_message.lower()

        # 1) Exercise technique / form questions (e.g., "how to do burpees")
        if (
            re.search(r"\bhow\s+(to|do)\b", message_lower)
            or any(k in message_lower for k in ["form", "technique", "tutorial", "proper form"]) 
            or any(k in message_lower for k in [
                "burpee", "push up", "push-up", "squat", "deadlift", "bench press",
                "plank", "lunge", "shoulder press", "row", "curl", "tricep dip"
            ])
        ):
            return self._exercise_instructions(message_lower, user)
        
        # Workout-related responses
        if any(word in message_lower for word in ['workout', 'exercise', 'train', 'gym', 'fitness']):
            if user and user.goal == 'lose_weight':
                return """💪 Perfect timing to ask! For weight loss, here's your workout plan:

**30-Minute Fat Burning Workout:**
1. Warm-up (5 min): Light jogging or jumping jacks
2. HIIT Circuit (20 min) - Do each for 45 sec, rest 15 sec:
   • Burpees
   • High knees
   • Mountain climbers
   • Jump squats
   • Push-ups
3. Cool-down (5 min): Stretching

**Frequency:** 4-5 times per week
**Tip:** Stay consistent and track your progress! 🔥"""
            
            elif user and user.goal == 'gain_muscle':
                return """💪 Let's build some muscle! Here's your workout:

**Strength Training (45 min):**
**Upper Body:**
• Bench Press: 4 sets x 8-10 reps
• Pull-ups: 4 sets x 6-8 reps
• Shoulder Press: 3 sets x 10 reps
• Bicep Curls: 3 sets x 12 reps

**Lower Body:**
• Squats: 4 sets x 8-10 reps
• Deadlifts: 4 sets x 6-8 reps
• Leg Press: 3 sets x 12 reps

**Frequency:** 4-5 days/week
**Pro Tip:** Eat protein within 30 min post-workout! 🏋️"""
            
            else:
                return """💪 Here's a balanced full-body workout for you:

**40-Minute Complete Workout:**
1. Warm-up (5 min): Dynamic stretching
2. Circuit (30 min) - 3 rounds:
   • Push-ups: 12 reps
   • Squats: 15 reps
   • Plank: 45 seconds
   • Lunges: 10 each leg
   • Dumbbell rows: 12 reps
   • Rest: 60 seconds
3. Cool-down (5 min): Static stretches

Do this 3-4 times weekly for best results! 💯"""
        
        # Nutrition/diet responses
        elif any(word in message_lower for word in ['food', 'eat', 'nutrition', 'diet', 'meal', 'calorie', 'protein']):
            if user and user.goal == 'lose_weight':
                return """🥗 Nutrition for Weight Loss:

**Daily Calorie Target:** ~500 kcal deficit from maintenance

**Meal Structure:**
• **Breakfast:** Oatmeal with berries + eggs
• **Lunch:** Grilled chicken salad with olive oil
• **Dinner:** Baked fish with vegetables
• **Snacks:** Greek yogurt, nuts (small portions)

**Key Rules:**
✅ Drink 3-4 liters water daily
✅ Protein at every meal (keeps you full)
✅ Avoid sugary drinks & processed foods
✅ Eat slowly, track portions

**Pro Tip:** Meal prep on Sundays for the week! 📝"""
            
            elif user and user.goal == 'gain_muscle':
                return """🥗 Nutrition for Muscle Gain:

**Daily Calorie Target:** ~300-500 kcal surplus

**Meal Structure (5-6 meals):**
• **Meal 1:** Eggs, oats, banana
• **Meal 2:** Chicken, rice, vegetables
• **Meal 3:** Tuna sandwich, apple
• **Meal 4 (Pre-workout):** Protein shake, banana
• **Meal 5 (Post-workout):** Chicken, sweet potato
• **Meal 6:** Cottage cheese, nuts

**Macros Target:**
• Protein: 1.6-2g per kg bodyweight
• Carbs: 4-6g per kg
• Fats: 1g per kg

**Muscle-Building Foods:** Chicken, eggs, fish, rice, oats, sweet potato 💪"""
            
            else:
                return """🥗 Balanced Nutrition Guide:

**Plate Method:**
• 1/2 plate: Vegetables (colorful!)
• 1/4 plate: Lean protein (chicken, fish, tofu)
• 1/4 plate: Complex carbs (brown rice, quinoa)
• Healthy fats: Olive oil, nuts, avocado

**Daily Essentials:**
✅ 8+ glasses water
✅ 5 servings fruits/vegetables
✅ Lean protein each meal
✅ Whole grains over refined
✅ Limit processed foods & sugar

**Sample Day:**
• Breakfast: Oats + banana + almonds
• Lunch: Grilled chicken salad
• Snack: Greek yogurt
• Dinner: Salmon + quinoa + veggies

Stay consistent and you'll see results! 🌟"""
        
        # Motivation responses
        elif any(word in message_lower for word in ['motivate', 'inspire', 'lazy', 'tired', 'give up', 'quit', 'hard']):
            return f"""🌟 Listen up, {user.name if user and user.name else 'Champion'}!

**Remember This:**
• You didn't come this far to only come this far
• Every workout counts, even the short ones
• Progress > Perfection
• You're stronger than your excuses

**Quick Motivation Boost:**
1. Think about WHY you started
2. Visualize your goal body/strength
3. Remember how good you feel AFTER working out
4. You'll regret NOT doing it, never regret doing it

**Right Now:** Put on your workout clothes. Once you're dressed, you're 90% there! 💪

The hardest part is starting - and you're already thinking about it. That's a win! Now GO! 🔥

You've got this! 💯"""
        
        # Progress/tips responses
        elif any(word in message_lower for word in ['progress', 'improve', 'better', 'tip', 'advice', 'help']):
            return """� Tips to Maximize Your Progress:

**Workout Tips:**
✅ Track everything (reps, weight, time)
✅ Progressive overload (increase gradually)
✅ Rest 48 hours between muscle groups
✅ Get 7-9 hours sleep
✅ Stay hydrated (3-4L water daily)

**Nutrition Tips:**
✅ Meal prep weekly
✅ Protein with every meal
✅ Don't skip breakfast
✅ Eat within 30 min post-workout
✅ Limit cheat meals to 1-2/week

**Mental Game:**
✅ Set SMART goals
✅ Take progress photos monthly
✅ Find a workout buddy
✅ Celebrate small wins
✅ Be patient - results take time

**Remember:** Consistency beats intensity! Show up even when motivation is low. 🎯"""
        
        # Default personalized response
        else:
            user_name = user.name if user and user.name else user.username if user else 'there'
            goal_text = ""
            if user and user.goal:
                goal_map = {
                    'lose_weight': 'weight loss',
                    'gain_muscle': 'muscle gain',
                    'maintain_weight': 'maintaining fitness'
                }
                goal_text = f" I see your goal is {goal_map.get(user.goal, 'fitness')}."
            
            return f"""👋 Hey {user_name}!{goal_text}

I'm your AI fitness coach, here to help with:

🏋️ **Workouts** - Custom plans for your goals
🥗 **Nutrition** - Meal plans and diet advice  
💪 **Motivation** - Keep you fired up
📊 **Progress** - Tips to see results faster

**Try asking me:**
• "Give me a workout for today"
• "What should I eat to reach my goal?"
• "I need motivation to stay consistent"
• "How can I see results faster?"

I'm here 24/7 to help you crush your fitness goals! What would you like to know? 💪"""

    def _exercise_instructions(self, message_lower, user=None):
        def steps(title, bullets, tips=None):
            tips_text = f"\n\nPro tips:\n- " + "\n- ".join(tips) if tips else ""
            return f"""📘 {title}

1) {bullets[0]}
2) {bullets[1]}
3) {bullets[2]}
4) {bullets[3]}
5) {bullets[4]}{tips_text}

Want a short demo GIF or common mistakes to avoid?"""

        if "burpee" in message_lower:
            return steps(
                "How to do a Burpee (full-body)",
                [
                    "Start standing, feet shoulder-width, core tight",
                    "Squat down and place hands on floor in front of you",
                    "Jump feet back into a plank (body straight, don’t sag)",
                    "Do an optional push-up, then jump feet back to hands",
                    "Explode upward into a jump, arms overhead"
                ],
                tips=[
                    "Keep your chest up as you drop into the squat",
                    "Brace your core during the plank to protect your lower back",
                    "Scale it: step back instead of jumping, or skip the push-up"
                ]
            )

        if "push" in message_lower and ("up" in message_lower or "push-up" in message_lower):
            return steps(
                "Proper Push-up Form",
                [
                    "Hands under shoulders, body in a straight line",
                    "Screw palms into the floor to engage lats",
                    "Lower chest towards floor, elbows ~45° from body",
                    "Keep core and glutes tight to avoid sagging",
                    "Press back up, fully extend without locking elbows"
                ],
                tips=["If tough, elevate hands on a bench; if easy, add tempo or weight"]
            )

        if "squat" in message_lower:
            return steps(
                "Bodyweight Squat Basics",
                [
                    "Stand shoulder-width, toes slightly out",
                    "Brace core and keep chest tall",
                    "Push hips back and bend knees, tracking over toes",
                    "Descend until thighs are at least parallel",
                    "Drive through mid-foot to stand up"
                ],
                tips=["Knees track with toes, don’t cave in; keep heels down"]
            )

        if "deadlift" in message_lower:
            return steps(
                "Conventional Deadlift Cues",
                [
                    "Feet hip-width, bar over mid-foot",
                    "Grip just outside knees, brace belly",
                    "Hips higher than squat, chest up, back neutral",
                    "Push floor away, bar stays close/shaves shins",
                    "Lock out by squeezing glutes, don’t lean back"
                ],
                tips=["If rounding, reduce load; think ‘proud chest’"]
            )

        if "bench" in message_lower and "press" in message_lower:
            return steps(
                "Barbell Bench Press Essentials",
                [
                    "Feet planted, slight arch, shoulder blades pinched",
                    "Grip so forearms are vertical at bottom",
                    "Unrack and set the bar over upper chest",
                    "Lower to mid/low chest, elbows ~45°",
                    "Press up, keep wrists straight and shoulder blades tight"
                ],
                tips=["Use a spotter; touch chest softly—don’t bounce"]
            )

        # Generic technique help
        return "🧭 Tell me the exercise name (e.g., burpees, squats, deadlift), and I’ll give you step-by-step form cues and tips!"
    
    def get_daily_motivation(self, user, recent_data=None):
        """Generate a personalized daily motivation message"""
        prompt = f"Give {user.name or user.username} a brief motivational message to start their day. Consider their goal: {user.goal}. Keep it to 2-3 sentences and inspiring! 💪"
        
        return self.chat(prompt, user, recent_data)
    
    def analyze_progress(self, user, weekly_data):
        """Analyze user's weekly progress and provide feedback"""
        prompt = f"""Analyze this week's fitness progress:
- Workouts completed: {weekly_data.get('workouts', 0)}
- Total calories burned: {weekly_data.get('calories_burned', 0)} kcal
- Habits completed: {weekly_data.get('habits_completed', 0)}
- Average daily water intake: {weekly_data.get('avg_water', 0)} ml

Provide brief feedback and suggestions for next week."""
        
        return self.chat(prompt, user, weekly_data)
    
    def suggest_workout(self, user, preferences=None):
        """Suggest a workout plan based on user goals and preferences"""
        prompt = "Suggest a workout routine for today based on my fitness goal and activity level. Include 3-4 exercises with sets/reps."
        
        if preferences:
            prompt += f" Preferences: {preferences}"
        
        return self.chat(prompt, user)
    
    def answer_nutrition_question(self, user, food_item):
        """Answer questions about specific foods"""
        prompt = f"Is {food_item} a good choice for my fitness goal? Give me brief nutrition info and how it fits my goals."
        
        return self.chat(prompt, user)


# Alternative: Use OpenAI-compatible API (if user has key)
class FitnessCoachOpenAI:
    """Alternative coach using OpenAI API (requires API key). Not used by default."""

    def __init__(self, api_key=None):
        """Initialize with OpenAI API key (only if package is installed)."""
        try:
            openai_mod = __import__('openai')
        except Exception:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")

        # Create client using dynamic module to avoid static import errors
        self.client = openai_mod.OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"

    def chat(self, user_message, user=None, recent_data=None):
        """Chat using OpenAI API (placeholder)."""
        raise NotImplementedError("FitnessCoachOpenAI is not wired in this project. Use FitnessCoach instead.")
