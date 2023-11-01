import time
import random

class Pet:
    class InvalidFoodError(Exception):
        """Raised when an invalid food is given to the pet."""
        pass

    class InvalidQuantityError(Exception):
        """Raised when the user gives too many or too little quantity"""
    
    HUNGER_RATE = 3
    THIRST_RATE = 4
    CLEANLINESS_RATE = 1
    MOOD_RATE = 2
    VALID_FOODS = {'meat':(15,5),'vegetable':(10,2),'ice cream':(5,15),'bread':(8,8)} #meal:(hunger fiil, mood increase)
    
    def __init__(self, name, type):
        if not isinstance(name, str) or not isinstance(type, str):
            raise ValueError("Name and type must be strings.")
        self.name = name
        self.type = type
        self.food_level = random.randint(55, 80)
        self.water_level = random.randint(55, 80)
        self.sanitation_level = random.randint(55, 80)
        self.mood_level = 90
        self.last_update_time = time.time()

    def get_mood(self):
        if 0 <= self.mood_level < 20:
            return f"{self.name} is sad and lonely..."
        elif 20 <= self.mood_level < 40:
            return f"{self.name} is sad..."
        elif 40 <= self.mood_level < 60:
            return f"{self.name} would like some more attention..."
        elif 60 <= self.mood_level < 80:
            return f"{self.name} is happy!"
        else:
            return f"{self.name} is excited and happy to be with you!"

    def get_updated_status(self):
        time_change = time.time() - self.last_update_time
        rate_of_change = time_change / 1800
        self.food_level = max(self.food_level - rate_of_change * Pet.HUNGER_RATE, 0)
        self.water_level = max(self.water_level - rate_of_change * Pet.THIRST_RATE, 0)
        self.sanitation_level = max(self.sanitation_level - rate_of_change * Pet.CLEANLINESS_RATE, 0)
        self.mood_level = max(self.mood_level - rate_of_change * Pet.MOOD_RATE, 0)
        self.last_update_time = time.time()
        return {
            "Pet": self.name,
            "Mood": self.get_mood(),
            "Hunger": self.food_level,
            "Thirst": self.water_level,
            "Cleanliness": self.sanitation_level
        }
    
    def print_status(self):
        status = self.get_updated_status()
        order = ["Pet","Mood","Hunger","Thirst","Cleanliness"]
        for key in order:
            print(key+":",status[key])

    def feed_pet(self,food,quantity):
        self.get_updated_status()
        if food not in Pet.VALID_FOODS:
            raise Pet.InvalidFoodError(f"'{food}' is not a valid food. Valid foods are: {', '.join(Pet.VALID_FOODS)}")
        if quantity>3 or quantity<1:
            raise Pet.InvalidQuantityError(f"'{quantity}' is not a valid quantity. Valid quantities are 1,2 and 3. Can't give your pet a stomachache!")
        if not isinstance(food,str) or not isinstance(quantity,int):
            raise ValueError("Food must be a string and quantity must be an int.")
        food_fill = Pet.VALID_FOODS[food][0]
        mood_increase = Pet.VALID_FOODS[food][1]
        self.food_level = min(self.food_level + (food_fill * quantity),100)
        self.mood_level = min(self.mood_level + (mood_increase * quantity),100)

        reactions = {
            "meat": f"{self.name} pounces on the steak and gobbles it up!",
            "vegetable": f"{self.name} finished the fragrant vegetables before you knew it!",
            "ice cream": f"The sweet treat draws a smile on {self.name}'s face! He appreciates that you wiped the leftover cream from his mouth.",
            "bread": f"Perfect toasty sandwich! A comfortable meal for {self.name}."
        }
        
        print(reactions.get(food, f"{self.name} enjoyed the meal!"))


        





    

