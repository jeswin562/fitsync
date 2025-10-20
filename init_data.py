from app import create_app, db
from app.models import User, Habit, Exercise, Food

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Add exercises
        exercises = [
            # Cardio
            Exercise(name='Running', category='Cardio', calories_per_minute=10.0, description='Outdoor or treadmill running'),
            Exercise(name='Cycling', category='Cardio', calories_per_minute=8.0, description='Stationary or outdoor cycling'),
            Exercise(name='Swimming', category='Cardio', calories_per_minute=9.0, description='Freestyle swimming'),
            Exercise(name='Jump Rope', category='Cardio', calories_per_minute=12.0, description='High-intensity rope jumping'),
            Exercise(name='Rowing', category='Cardio', calories_per_minute=8.5, description='Rowing machine workout'),
            
            # Strength Training
            Exercise(name='Push-ups', category='Strength', calories_per_minute=7.0, description='Bodyweight chest exercise'),
            Exercise(name='Squats', category='Strength', calories_per_minute=6.0, description='Bodyweight leg exercise'),
            Exercise(name='Pull-ups', category='Strength', calories_per_minute=8.0, description='Upper body strength'),
            Exercise(name='Planks', category='Strength', calories_per_minute=4.0, description='Core stability exercise'),
            Exercise(name='Lunges', category='Strength', calories_per_minute=6.5, description='Leg strength and balance'),
            
            # Yoga & Flexibility
            Exercise(name='Yoga', category='Flexibility', calories_per_minute=3.0, description='Gentle yoga flow'),
            Exercise(name='Power Yoga', category='Flexibility', calories_per_minute=6.0, description='Intense yoga workout'),
            Exercise(name='Stretching', category='Flexibility', calories_per_minute=2.5, description='Basic stretching routine'),
            
            # Sports
            Exercise(name='Basketball', category='Sports', calories_per_minute=8.5, description='Basketball game'),
            Exercise(name='Tennis', category='Sports', calories_per_minute=7.5, description='Tennis match'),
            Exercise(name='Football', category='Sports', calories_per_minute=9.0, description='Football/soccer game'),
            Exercise(name='Cricket', category='Sports', calories_per_minute=5.0, description='Cricket match'),
            Exercise(name='Badminton', category='Sports', calories_per_minute=6.5, description='Badminton game'),
            
            # Dance
            Exercise(name='Zumba', category='Dance', calories_per_minute=8.0, description='Latin dance fitness'),
            Exercise(name='Bollywood Dance', category='Dance', calories_per_minute=7.5, description='Indian dance workout'),
            Exercise(name='Hip Hop', category='Dance', calories_per_minute=8.5, description='Hip hop dance class'),
            
            # Walking
            Exercise(name='Walking', category='Walking', calories_per_minute=4.0, description='Brisk walking'),
            Exercise(name='Power Walking', category='Walking', calories_per_minute=6.0, description='Fast-paced walking'),
            Exercise(name='Hiking', category='Walking', calories_per_minute=7.0, description='Trail hiking'),
        ]
        
        # Add comprehensive Indian foods
        foods = [
            # Breakfast Items
            Food(name='Idli', category='Breakfast', calories_per_serving=39, serving_size='1 piece (30g)', description='Steamed rice cakes'),
            Food(name='Dosa', category='Breakfast', calories_per_serving=133, serving_size='1 dosa (50g)', description='Crispy rice crepe'),
            Food(name='Upma', category='Breakfast', calories_per_serving=150, serving_size='1 cup (100g)', description='Semolina breakfast'),
            Food(name='Poha', category='Breakfast', calories_per_serving=120, serving_size='1 cup (100g)', description='Flattened rice breakfast'),
            Food(name='Paratha', category='Breakfast', calories_per_serving=180, serving_size='1 piece (50g)', description='Whole wheat flatbread'),
            Food(name='Aloo Paratha', category='Breakfast', calories_per_serving=250, serving_size='1 piece (80g)', description='Potato stuffed flatbread'),
            Food(name='Puri', category='Breakfast', calories_per_serving=120, serving_size='1 piece (25g)', description='Deep-fried bread'),
            Food(name='Bread Omelette', category='Breakfast', calories_per_serving=200, serving_size='1 serving', description='Egg omelette with bread'),
            Food(name='Masala Dosa', category='Breakfast', calories_per_serving=200, serving_size='1 dosa (80g)', description='Spiced potato dosa'),
            Food(name='Vada', category='Breakfast', calories_per_serving=150, serving_size='1 piece (40g)', description='Lentil fritter'),
            
            # Rice Dishes
            Food(name='Basmati Rice', category='Rice', calories_per_serving=121, serving_size='1/2 cup cooked (100g)', description='Aromatic long-grain rice'),
            Food(name='Biryani', category='Rice', calories_per_serving=350, serving_size='1 cup (200g)', description='Spiced rice with meat/vegetables'),
            Food(name='Pulao', category='Rice', calories_per_serving=280, serving_size='1 cup (200g)', description='Mixed vegetable rice'),
            Food(name='Jeera Rice', category='Rice', calories_per_serving=150, serving_size='1 cup (150g)', description='Cumin-flavored rice'),
            Food(name='Lemon Rice', category='Rice', calories_per_serving=180, serving_size='1 cup (150g)', description='Tangy lemon rice'),
            Food(name='Tomato Rice', category='Rice', calories_per_serving=200, serving_size='1 cup (150g)', description='Tomato-flavored rice'),
            Food(name='Curd Rice', category='Rice', calories_per_serving=160, serving_size='1 cup (150g)', description='Yogurt rice'),
            Food(name='Fried Rice', category='Rice', calories_per_serving=250, serving_size='1 cup (150g)', description='Chinese-style fried rice'),
            
            # Breads
            Food(name='Roti', category='Bread', calories_per_serving=80, serving_size='1 piece (30g)', description='Whole wheat flatbread'),
            Food(name='Naan', category='Bread', calories_per_serving=150, serving_size='1 piece (50g)', description='Leavened flatbread'),
            Food(name='Chapati', category='Bread', calories_per_serving=70, serving_size='1 piece (25g)', description='Whole wheat flatbread'),
            Food(name='Phulka', category='Bread', calories_per_serving=60, serving_size='1 piece (20g)', description='Puffed whole wheat bread'),
            Food(name='Bhatura', category='Bread', calories_per_serving=200, serving_size='1 piece (60g)', description='Deep-fried leavened bread'),
            Food(name='Kulcha', category='Bread', calories_per_serving=180, serving_size='1 piece (50g)', description='Stuffed leavened bread'),
            Food(name='Missi Roti', category='Bread', calories_per_serving=120, serving_size='1 piece (40g)', description='Gram flour flatbread'),
            Food(name='Makki ki Roti', category='Bread', calories_per_serving=100, serving_size='1 piece (35g)', description='Corn flour flatbread'),
            
            # Curries & Gravies
            Food(name='Butter Chicken', category='Curry', calories_per_serving=350, serving_size='1 cup (200g)', description='Creamy tomato-based chicken curry'),
            Food(name='Paneer Butter Masala', category='Curry', calories_per_serving=320, serving_size='1 cup (200g)', description='Cottage cheese in creamy gravy'),
            Food(name='Dal Makhani', category='Curry', calories_per_serving=280, serving_size='1 cup (200g)', description='Creamy black lentil curry'),
            Food(name='Rajma Masala', category='Curry', calories_per_serving=250, serving_size='1 cup (200g)', description='Kidney bean curry'),
            Food(name='Chana Masala', category='Curry', calories_per_serving=220, serving_size='1 cup (200g)', description='Chickpea curry'),
            Food(name='Aloo Gobi', category='Curry', calories_per_serving=180, serving_size='1 cup (200g)', description='Potato and cauliflower curry'),
            Food(name='Baingan Bharta', category='Curry', calories_per_serving=160, serving_size='1 cup (200g)', description='Roasted eggplant curry'),
            Food(name='Palak Paneer', category='Curry', calories_per_serving=280, serving_size='1 cup (200g)', description='Spinach with cottage cheese'),
            Food(name='Mushroom Masala', category='Curry', calories_per_serving=200, serving_size='1 cup (200g)', description='Mushroom curry'),
            Food(name='Mixed Vegetable Curry', category='Curry', calories_per_serving=180, serving_size='1 cup (200g)', description='Assorted vegetables in gravy'),
            
            # Tandoori & Grilled
            Food(name='Tandoori Chicken', category='Tandoori', calories_per_serving=280, serving_size='1 piece (100g)', description='Marinated grilled chicken'),
            Food(name='Seekh Kebab', category='Tandoori', calories_per_serving=200, serving_size='1 kebab (80g)', description='Minced meat kebab'),
            Food(name='Tandoori Fish', category='Tandoori', calories_per_serving=180, serving_size='1 piece (100g)', description='Grilled fish'),
            Food(name='Tandoori Paneer', category='Tandoori', calories_per_serving=220, serving_size='1 piece (80g)', description='Grilled cottage cheese'),
            Food(name='Chicken Tikka', category='Tandoori', calories_per_serving=250, serving_size='1 piece (100g)', description='Marinated chicken pieces'),
            Food(name='Malai Kebab', category='Tandoori', calories_per_serving=280, serving_size='1 kebab (80g)', description='Creamy chicken kebab'),
            
            # Street Food
            Food(name='Samosa', category='Street Food', calories_per_serving=250, serving_size='1 piece (60g)', description='Spiced potato pastry'),
            Food(name='Pakora', category='Street Food', calories_per_serving=180, serving_size='1 piece (40g)', description='Vegetable fritter'),
            Food(name='Bhel Puri', category='Street Food', calories_per_serving=200, serving_size='1 cup (100g)', description='Puffed rice snack'),
            Food(name='Pani Puri', category='Street Food', calories_per_serving=150, serving_size='6 pieces', description='Water-filled crispy puris'),
            Food(name='Vada Pav', category='Street Food', calories_per_serving=300, serving_size='1 serving', description='Potato fritter sandwich'),
            Food(name='Dahi Puri', category='Street Food', calories_per_serving=280, serving_size='1 serving', description='Yogurt-filled puris'),
            Food(name='Ragda Pattice', category='Street Food', calories_per_serving=320, serving_size='1 serving', description='Potato patty with white peas'),
            Food(name='Kachori', category='Street Food', calories_per_serving=220, serving_size='1 piece (50g)', description='Spiced lentil pastry'),
            Food(name='Chaat', category='Street Food', calories_per_serving=250, serving_size='1 serving', description='Mixed savory snack'),
            Food(name='Pav Bhaji', category='Street Food', calories_per_serving=350, serving_size='1 serving', description='Bread with vegetable curry'),
            
            # Sweets & Desserts
            Food(name='Gulab Jamun', category='Dessert', calories_per_serving=150, serving_size='1 piece (25g)', description='Sweet milk dumpling'),
            Food(name='Rasgulla', category='Dessert', calories_per_serving=120, serving_size='1 piece (30g)', description='Sweet cottage cheese ball'),
            Food(name='Jalebi', category='Dessert', calories_per_serving=180, serving_size='1 piece (40g)', description='Crispy sweet spiral'),
            Food(name='Ladoo', category='Dessert', calories_per_serving=200, serving_size='1 piece (35g)', description='Sweet gram flour ball'),
            Food(name='Barfi', category='Dessert', calories_per_serving=160, serving_size='1 piece (25g)', description='Milk-based sweet'),
            Food(name='Kheer', category='Dessert', calories_per_serving=220, serving_size='1 cup (100g)', description='Rice pudding'),
            Food(name='Rasmalai', category='Dessert', calories_per_serving=180, serving_size='1 piece (40g)', description='Cottage cheese in sweet milk'),
            Food(name='Gajar ka Halwa', category='Dessert', calories_per_serving=250, serving_size='1 cup (100g)', description='Carrot pudding'),
            Food(name='Kulfi', category='Dessert', calories_per_serving=200, serving_size='1 piece (80g)', description='Indian ice cream'),
            Food(name='Shrikhand', category='Dessert', calories_per_serving=180, serving_size='1 cup (100g)', description='Sweetened yogurt dessert'),
            
            # Beverages
            Food(name='Masala Chai', category='Beverage', calories_per_serving=80, serving_size='1 cup (200ml)', description='Spiced Indian tea'),
            Food(name='Lassi', category='Beverage', calories_per_serving=120, serving_size='1 glass (250ml)', description='Sweet yogurt drink'),
            Food(name='Mango Lassi', category='Beverage', calories_per_serving=180, serving_size='1 glass (250ml)', description='Mango yogurt drink'),
            Food(name='Thandai', category='Beverage', calories_per_serving=200, serving_size='1 glass (250ml)', description='Nut and spice milk drink'),
            Food(name='Filter Coffee', category='Beverage', calories_per_serving=60, serving_size='1 cup (150ml)', description='South Indian filter coffee'),
            Food(name='Jaljeera', category='Beverage', calories_per_serving=40, serving_size='1 glass (200ml)', description='Spiced cumin water'),
            Food(name='Nimbu Pani', category='Beverage', calories_per_serving=50, serving_size='1 glass (200ml)', description='Lemon water'),
            Food(name='Coconut Water', category='Beverage', calories_per_serving=45, serving_size='1 glass (250ml)', description='Fresh coconut water'),
            
            # Snacks
            Food(name='Murukku', category='Snack', calories_per_serving=120, serving_size='1 piece (20g)', description='Rice flour snack'),
            Food(name='Mixture', category='Snack', calories_per_serving=150, serving_size='1 cup (50g)', description='Mixed savory snack'),
            Food(name='Kurkure', category='Snack', calories_per_serving=140, serving_size='1 cup (30g)', description='Spicy corn snack'),
            Food(name='Chevda', category='Snack', calories_per_serving=160, serving_size='1 cup (50g)', description='Flattened rice snack'),
            Food(name='Roasted Peanuts', category='Snack', calories_per_serving=160, serving_size='1/4 cup (30g)', description='Dry roasted peanuts'),
            Food(name='Masala Peanuts', category='Snack', calories_per_serving=180, serving_size='1/4 cup (30g)', description='Spiced peanuts'),
            Food(name='Bombay Mix', category='Snack', calories_per_serving=170, serving_size='1 cup (50g)', description='Mixed savory snack'),
            Food(name='Aloo Bhujia', category='Snack', calories_per_serving=130, serving_size='1 cup (30g)', description='Potato snack'),
            
            # Pickles & Chutneys
            Food(name='Mango Pickle', category='Condiment', calories_per_serving=80, serving_size='1 tbsp (15g)', description='Spicy mango pickle'),
            Food(name='Lemon Pickle', category='Condiment', calories_per_serving=60, serving_size='1 tbsp (15g)', description='Tangy lemon pickle'),
            Food(name='Mint Chutney', category='Condiment', calories_per_serving=30, serving_size='1 tbsp (15g)', description='Fresh mint chutney'),
            Food(name='Coconut Chutney', category='Condiment', calories_per_serving=50, serving_size='1 tbsp (15g)', description='Coconut and chutney'),
            Food(name='Tamarind Chutney', category='Condiment', calories_per_serving=40, serving_size='1 tbsp (15g)', description='Sweet tamarind chutney'),
            Food(name='Onion Chutney', category='Condiment', calories_per_serving=25, serving_size='1 tbsp (15g)', description='Spicy onion chutney'),
            
            # Regional Specialties
            Food(name='Dosa Sambar', category='Regional', calories_per_serving=280, serving_size='1 serving', description='Dosa with lentil soup'),
            Food(name='Rasam', category='Regional', calories_per_serving=80, serving_size='1 cup (200ml)', description='Spicy tamarind soup'),
            Food(name='Sambar', category='Regional', calories_per_serving=120, serving_size='1 cup (200ml)', description='Lentil vegetable soup'),
            Food(name='Raita', category='Regional', calories_per_serving=60, serving_size='1 cup (100g)', description='Yogurt with vegetables'),
            Food(name='Papad', category='Regional', calories_per_serving=40, serving_size='1 piece (10g)', description='Crispy lentil wafer'),
            Food(name='Achar', category='Regional', calories_per_serving=70, serving_size='1 tbsp (15g)', description='Mixed vegetable pickle'),
            Food(name='Chutney', category='Regional', calories_per_serving=35, serving_size='1 tbsp (15g)', description='Spicy condiment'),
            Food(name='Pachadi', category='Regional', calories_per_serving=80, serving_size='1 cup (100g)', description='South Indian yogurt dish'),
        ]
        
        # Add to database
        for exercise in exercises:
            db.session.add(exercise)
        
        for food in foods:
            db.session.add(food)
        
        db.session.commit()
        print("Database initialized with exercise and food data!")

if __name__ == '__main__':
    init_db() 