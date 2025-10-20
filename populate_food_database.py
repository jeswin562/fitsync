"""
Populate the fitness tracker with a comprehensive food database
Run this script once to add hundreds of common foods with accurate nutritional data
"""

from app import create_app, db
from app.models import Food

app = create_app()

# Comprehensive food database organized by category
COMPREHENSIVE_FOODS = {
    # BREAKFAST FOODS
    'Breakfast': [
        ('Scrambled Eggs', 140, '2 eggs', 'Protein-rich breakfast'),
        ('Fried Egg', 90, '1 large egg', 'Quick protein source'),
        ('Boiled Egg', 68, '1 large egg', 'High protein, low calorie'),
        ('Egg White Omelette', 100, '3 egg whites', 'Low-fat protein option'),
        ('French Toast', 150, '1 slice', 'Sweet breakfast option'),
        ('Pancakes', 175, '2 medium (100g)', 'Classic breakfast'),
        ('Waffles', 200, '1 waffle (75g)', 'Belgian-style waffle'),
        ('Oatmeal', 150, '1 cup cooked (240g)', 'High fiber breakfast'),
        ('Granola', 250, '1/2 cup (60g)', 'Crunchy cereal'),
        ('Corn Flakes', 100, '1 cup (30g)', 'Light cereal'),
        ('Muesli', 200, '1/2 cup (60g)', 'Mixed grain cereal'),
        ('Bread Toast', 80, '1 slice (30g)', 'Whole wheat toast'),
        ('Bagel', 245, '1 medium (90g)', 'Dense bread ring'),
        ('Croissant', 230, '1 medium (60g)', 'Buttery pastry'),
        ('English Muffin', 130, '1 muffin (60g)', 'Split and toasted'),
        ('Peanut Butter Toast', 190, '1 slice with 1 tbsp PB', 'High protein toast'),
        ('Avocado Toast', 220, '1 slice with 1/4 avocado', 'Healthy fats'),
        ('Greek Yogurt', 100, '1 cup (170g)', 'High protein yogurt'),
        ('Regular Yogurt', 150, '1 cup (245g)', 'Creamy dairy'),
        ('Smoothie Bowl', 300, '1 bowl (350g)', 'Blended fruit bowl'),
        ('Protein Shake', 150, '1 scoop (30g)', 'Post-workout drink'),
    ],
    
    # INDIAN BREAKFAST
    'Indian Breakfast': [
        ('Idli', 35, '1 piece (40g)', 'Steamed rice cake'),
        ('Dosa', 120, '1 piece (50g)', 'Rice and lentil crepe'),
        ('Masala Dosa', 250, '1 piece (150g)', 'Dosa with potato filling'),
        ('Puri', 150, '1 piece (25g)', 'Deep fried bread'),
        ('Paratha', 180, '1 piece (60g)', 'Stuffed flatbread'),
        ('Aloo Paratha', 250, '1 piece (100g)', 'Potato stuffed paratha'),
        ('Upma', 200, '1 cup (150g)', 'Semolina breakfast'),
        ('Poha', 180, '1 cup (150g)', 'Flattened rice dish'),
        ('Medu Vada', 180, '1 piece (60g)', 'Fried lentil donut'),
        ('Sambar', 80, '1 cup (240ml)', 'Lentil vegetable stew'),
        ('Coconut Chutney', 60, '2 tbsp (30g)', 'Coconut condiment'),
        ('Chole Bhature', 450, '1 plate', 'Chickpea curry with fried bread'),
        ('Pongal', 200, '1 cup (150g)', 'Rice and lentil porridge'),
        ('Uttapam', 180, '1 piece (80g)', 'Thick rice pancake'),
    ],
    
    # MAIN COURSE
    'Main Course': [
        ('White Rice', 130, '1 cup cooked (150g)', 'Plain steamed rice'),
        ('Brown Rice', 110, '1 cup cooked (150g)', 'Whole grain rice'),
        ('Basmati Rice', 140, '1 cup cooked (150g)', 'Aromatic rice'),
        ('Fried Rice', 230, '1 cup (150g)', 'Stir-fried rice'),
        ('Jeera Rice', 160, '1 cup (150g)', 'Cumin flavored rice'),
        ('Roti', 80, '1 piece (30g)', 'Whole wheat flatbread'),
        ('Chapati', 70, '1 piece (25g)', 'Thin flatbread'),
        ('Naan', 140, '1 piece (60g)', 'Leavened flatbread'),
        ('Garlic Naan', 160, '1 piece (65g)', 'Naan with garlic'),
        ('Dal', 120, '1 cup (150g)', 'Lentil curry'),
        ('Dal Makhani', 200, '1 cup (150g)', 'Creamy black lentil curry'),
        ('Rajma', 180, '1 cup (150g)', 'Kidney bean curry'),
        ('Chicken Curry', 250, '1 cup (150g)', 'Chicken in gravy'),
        ('Butter Chicken', 320, '1 cup (150g)', 'Creamy tomato chicken'),
        ('Chicken Tikka', 200, '6 pieces (150g)', 'Grilled chicken pieces'),
        ('Tandoori Chicken', 220, '1 quarter (150g)', 'Clay oven roasted chicken'),
        ('Paneer Curry', 280, '1 cup (150g)', 'Cottage cheese curry'),
        ('Palak Paneer', 260, '1 cup (150g)', 'Spinach paneer curry'),
        ('Paneer Tikka', 240, '6 pieces (150g)', 'Grilled paneer cubes'),
        ('Aloo Gobi', 180, '1 cup (150g)', 'Potato cauliflower curry'),
        ('Mixed Vegetable Curry', 150, '1 cup (150g)', 'Various vegetables in gravy'),
        ('Biryani', 350, '1 cup (200g)', 'Spiced rice with meat'),
        ('Vegetable Biryani', 300, '1 cup (200g)', 'Spiced rice with vegetables'),
        ('Mutton Curry', 280, '1 cup (150g)', 'Lamb in gravy'),
        ('Fish Curry', 180, '1 cup (150g)', 'Fish in spiced gravy'),
        ('Egg Curry', 200, '2 eggs in gravy (150g)', 'Boiled eggs in curry'),
    ],
    
    # SNACKS
    'Snacks': [
        ('Samosa', 250, '1 piece (60g)', 'Fried pastry with filling'),
        ('Pakora', 180, '1 piece (30g)', 'Fried vegetable fritters'),
        ('Bhel Puri', 200, '1 cup (100g)', 'Puffed rice snack'),
        ('Pani Puri', 300, '1 plate (150g)', 'Crispy hollow shells'),
        ('Chaat', 300, '1 plate (150g)', 'Mixed savory snack'),
        ('Vada Pav', 280, '1 piece (150g)', 'Potato fritter in bun'),
        ('Pav Bhaji', 350, '1 plate', 'Mashed vegetables with bread'),
        ('French Fries', 320, '1 medium (150g)', 'Deep fried potato strips'),
        ('Potato Chips', 150, '1 oz (28g)', 'Thin fried potato slices'),
        ('Popcorn', 30, '1 cup air-popped (8g)', 'Popped corn kernels'),
        ('Pretzels', 110, '1 oz (28g)', 'Baked twisted snack'),
        ('Crackers', 120, '5 crackers (30g)', 'Crispy baked snack'),
        ('Cheese Cubes', 115, '1 oz (28g)', 'Cheddar cheese'),
        ('String Cheese', 80, '1 piece (28g)', 'Mozzarella stick'),
        ('Trail Mix', 140, '1/4 cup (30g)', 'Nuts and dried fruit'),
        ('Energy Bar', 200, '1 bar (50g)', 'Granola/protein bar'),
        ('Protein Bar', 180, '1 bar (50g)', 'High protein snack bar'),
        ('Nuts Mix', 170, '1/4 cup (30g)', 'Mixed nuts'),
        ('Almonds', 160, '1/4 cup (30g)', 'Raw almonds'),
        ('Cashews', 155, '1/4 cup (30g)', 'Roasted cashews'),
        ('Walnuts', 185, '1/4 cup (30g)', 'Walnut halves'),
        ('Peanuts', 160, '1/4 cup (30g)', 'Roasted peanuts'),
        ('Pistachios', 160, '1/4 cup (30g)', 'Shelled pistachios'),
    ],
    
    # FRUITS
    'Fruits': [
        ('Apple', 95, '1 medium (180g)', 'Fresh apple'),
        ('Banana', 105, '1 medium (120g)', 'Yellow banana'),
        ('Orange', 62, '1 medium (130g)', 'Fresh orange'),
        ('Grapes', 104, '1 cup (150g)', 'Green or red grapes'),
        ('Strawberries', 49, '1 cup (150g)', 'Fresh strawberries'),
        ('Blueberries', 84, '1 cup (150g)', 'Fresh blueberries'),
        ('Watermelon', 46, '1 cup diced (150g)', 'Seedless watermelon'),
        ('Mango', 200, '1 cup diced (165g)', 'Sweet tropical fruit'),
        ('Pineapple', 82, '1 cup diced (165g)', 'Fresh pineapple chunks'),
        ('Papaya', 62, '1 cup diced (150g)', 'Ripe papaya'),
        ('Pomegranate', 144, '1 cup seeds (175g)', 'Pomegranate arils'),
        ('Kiwi', 42, '1 medium (70g)', 'Green kiwifruit'),
        ('Pear', 102, '1 medium (180g)', 'Fresh pear'),
        ('Peach', 59, '1 medium (150g)', 'Fresh peach'),
        ('Plum', 30, '1 medium (65g)', 'Fresh plum'),
        ('Cherries', 97, '1 cup (150g)', 'Sweet cherries'),
        ('Guava', 112, '1 cup (165g)', 'Fresh guava'),
        ('Lychee', 125, '1 cup (190g)', 'Fresh lychees'),
        ('Dragon Fruit', 102, '1 cup (227g)', 'White or red dragon fruit'),
        ('Coconut', 283, '1 cup shredded (80g)', 'Fresh coconut meat'),
    ],
    
    # VEGETABLES
    'Vegetables': [
        ('Broccoli', 55, '1 cup cooked (150g)', 'Steamed broccoli'),
        ('Cauliflower', 25, '1 cup cooked (150g)', 'Steamed cauliflower'),
        ('Spinach', 41, '1 cup cooked (180g)', 'Cooked spinach'),
        ('Kale', 33, '1 cup cooked (130g)', 'Cooked kale'),
        ('Carrots', 52, '1 cup cooked (150g)', 'Boiled carrots'),
        ('Bell Pepper', 39, '1 cup chopped (150g)', 'Red/green pepper'),
        ('Tomato', 22, '1 medium (120g)', 'Fresh tomato'),
        ('Cucumber', 16, '1 cup sliced (120g)', 'Fresh cucumber'),
        ('Lettuce', 5, '1 cup shredded (50g)', 'Iceberg lettuce'),
        ('Cabbage', 22, '1 cup chopped (90g)', 'Raw cabbage'),
        ('Green Beans', 44, '1 cup cooked (150g)', 'Steamed beans'),
        ('Peas', 134, '1 cup cooked (150g)', 'Green peas'),
        ('Corn', 143, '1 cup (150g)', 'Sweet corn kernels'),
        ('Potato', 163, '1 medium boiled (150g)', 'Boiled potato'),
        ('Sweet Potato', 112, '1 medium baked (150g)', 'Baked sweet potato'),
        ('Onion', 44, '1 medium (110g)', 'Raw onion'),
        ('Garlic', 4, '1 clove (3g)', 'Fresh garlic'),
        ('Ginger', 5, '1 tbsp (6g)', 'Fresh ginger'),
        ('Mushrooms', 22, '1 cup sliced (70g)', 'White mushrooms'),
        ('Eggplant', 35, '1 cup cooked (100g)', 'Cooked eggplant'),
    ],
    
    # DESSERTS
    'Desserts': [
        ('Gulab Jamun', 150, '1 piece (25g)', 'Sweet milk dumpling'),
        ('Rasgulla', 120, '1 piece (30g)', 'Sweet cheese ball'),
        ('Jalebi', 200, '1 piece (40g)', 'Sweet pretzel'),
        ('Kheer', 250, '1 cup (150g)', 'Rice pudding'),
        ('Gajar Halwa', 280, '1 cup (150g)', 'Carrot dessert'),
        ('Ladoo', 120, '1 piece (30g)', 'Sweet ball'),
        ('Barfi', 100, '1 piece (25g)', 'Milk fudge'),
        ('Kulfi', 140, '1 piece (80ml)', 'Indian ice cream'),
        ('Ice Cream', 137, '1/2 cup (70g)', 'Vanilla ice cream'),
        ('Chocolate Ice Cream', 143, '1/2 cup (70g)', 'Chocolate flavor'),
        ('Cake', 235, '1 slice (80g)', 'Vanilla cake with frosting'),
        ('Chocolate Cake', 352, '1 slice (95g)', 'Rich chocolate cake'),
        ('Brownie', 112, '1 square (24g)', 'Chocolate brownie'),
        ('Cookie', 50, '1 medium (12g)', 'Chocolate chip cookie'),
        ('Donut', 250, '1 medium (60g)', 'Glazed donut'),
        ('Muffin', 425, '1 large (120g)', 'Blueberry muffin'),
        ('Cupcake', 305, '1 medium (80g)', 'Frosted cupcake'),
        ('Pie', 296, '1 slice (125g)', 'Apple pie'),
        ('Cheesecake', 321, '1 slice (100g)', 'New York cheesecake'),
        ('Pudding', 150, '1/2 cup (140g)', 'Chocolate pudding'),
        ('Chocolate Bar', 235, '1 bar (45g)', 'Milk chocolate'),
        ('Dark Chocolate', 170, '1 oz (28g)', '70% cacao dark chocolate'),
    ],
    
    # BEVERAGES
    'Beverages': [
        ('Water', 0, '1 glass (240ml)', 'Plain water'),
        ('Masala Chai', 80, '1 cup (200ml)', 'Spiced tea with milk'),
        ('Black Tea', 2, '1 cup (240ml)', 'Plain black tea'),
        ('Green Tea', 2, '1 cup (240ml)', 'Brewed green tea'),
        ('Coffee', 5, '1 cup (240ml)', 'Black coffee'),
        ('Coffee with Milk', 40, '1 cup (240ml)', 'Coffee with whole milk'),
        ('Cappuccino', 80, '1 cup (240ml)', 'Espresso with steamed milk'),
        ('Latte', 120, '1 cup (240ml)', 'Milk-heavy coffee'),
        ('Milk', 120, '1 glass (250ml)', 'Full fat milk'),
        ('Skim Milk', 83, '1 glass (250ml)', 'Fat-free milk'),
        ('Almond Milk', 30, '1 glass (250ml)', 'Unsweetened almond milk'),
        ('Lassi', 120, '1 glass (250ml)', 'Yogurt drink'),
        ('Mango Lassi', 200, '1 glass (250ml)', 'Mango yogurt drink'),
        ('Fresh Juice', 110, '1 glass (250ml)', 'Orange juice'),
        ('Apple Juice', 115, '1 glass (250ml)', '100% apple juice'),
        ('Mango Juice', 140, '1 glass (250ml)', 'Mango nectar'),
        ('Coconut Water', 46, '1 glass (250ml)', 'Fresh coconut water'),
        ('Soda', 140, '1 can (355ml)', 'Cola soft drink'),
        ('Sports Drink', 80, '1 bottle (500ml)', 'Electrolyte beverage'),
        ('Energy Drink', 110, '1 can (250ml)', 'Caffeinated energy drink'),
        ('Smoothie', 200, '1 glass (250ml)', 'Fruit smoothie'),
        ('Protein Shake', 150, '1 scoop (30g)', 'Whey protein shake'),
    ],
    
    # FAST FOOD
    'Fast Food': [
        ('Hamburger', 250, '1 burger (100g)', 'Basic beef burger'),
        ('Cheeseburger', 300, '1 burger (120g)', 'Burger with cheese'),
        ('Big Mac', 550, '1 burger (215g)', 'Double-decker burger'),
        ('Pizza Slice', 285, '1 slice (125g)', 'Regular cheese pizza'),
        ('Pepperoni Pizza', 313, '1 slice (125g)', 'With pepperoni'),
        ('Hot Dog', 290, '1 frank with bun (100g)', 'Beef hot dog'),
        ('Fried Chicken', 320, '1 piece (150g)', 'Crispy fried chicken'),
        ('Chicken Nuggets', 280, '6 pieces (100g)', 'Breaded chicken nuggets'),
        ('Chicken Wings', 240, '4 pieces (120g)', 'Buffalo wings'),
        ('Sub Sandwich', 410, '6 inch sub (200g)', 'Turkey sub'),
        ('Tacos', 170, '1 taco (100g)', 'Beef taco'),
        ('Burrito', 470, '1 burrito (250g)', 'Bean and cheese burrito'),
        ('Nachos', 350, '1 serving (150g)', 'Chips with cheese'),
        ('Onion Rings', 320, '1 serving (100g)', 'Fried onion rings'),
        ('Mozzarella Sticks', 300, '5 pieces (120g)', 'Fried cheese sticks'),
    ],
    
    # PROTEIN SOURCES
    'Protein': [
        ('Chicken Breast', 165, '100g cooked', 'Skinless, boneless'),
        ('Chicken Thigh', 209, '100g cooked', 'With skin'),
        ('Ground Beef', 250, '100g cooked', '80% lean'),
        ('Lean Beef', 183, '100g cooked', '95% lean'),
        ('Pork Chop', 231, '100g cooked', 'Lean cut'),
        ('Bacon', 541, '100g cooked', 'Crispy bacon'),
        ('Salmon', 206, '100g cooked', 'Atlantic salmon'),
        ('Tuna', 130, '100g cooked', 'Yellowfin tuna'),
        ('Shrimp', 99, '100g cooked', 'Peeled shrimp'),
        ('Tilapia', 129, '100g cooked', 'White fish'),
        ('Tofu', 76, '100g', 'Firm tofu'),
        ('Cottage Cheese', 98, '100g', 'Low-fat cottage cheese'),
        ('Paneer', 265, '100g', 'Indian cottage cheese'),
        ('Protein Powder', 120, '1 scoop (30g)', 'Whey protein isolate'),
    ],
}

def populate_food_database():
    """Add comprehensive food database to the application"""
    with app.app_context():
        # Check if database already has many foods (avoid duplicates)
        existing_count = Food.query.count()
        if existing_count > 50:
            print(f"Database already has {existing_count} foods.")
            response = input("Do you want to add more foods anyway? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted. No changes made.")
                return
        
        total_added = 0
        
        for category, foods in COMPREHENSIVE_FOODS.items():
            print(f"\nAdding {category} items...")
            for name, calories, serving, description in foods:
                # Check if food already exists
                existing = Food.query.filter_by(name=name, category=category).first()
                if existing:
                    print(f"  - {name} already exists, skipping...")
                    continue
                
                food = Food(
                    name=name,
                    category=category,
                    calories_per_serving=calories,
                    serving_size=serving,
                    description=description
                )
                db.session.add(food)
                total_added += 1
                print(f"  + Added: {name} ({calories} cal / {serving})")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully added {total_added} new foods to the database!")
            print(f"Total foods in database: {Food.query.count()}")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error adding foods: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("COMPREHENSIVE FOOD DATABASE POPULATOR")
    print("=" * 60)
    print("\nThis will add 200+ foods to your database including:")
    print("  - Breakfast foods (American & Indian)")
    print("  - Main course meals")
    print("  - Snacks and appetizers")
    print("  - Fruits and vegetables")
    print("  - Desserts")
    print("  - Beverages")
    print("  - Fast food")
    print("  - Protein sources")
    print("\n" + "=" * 60)
    
    populate_food_database()
