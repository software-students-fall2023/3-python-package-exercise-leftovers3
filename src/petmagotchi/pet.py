import time
import random

class Pet:
    HUNGER_RATE = 3
    THIRST_RATE = 4
    CLEANLINESS_RATE = 1
    MOOD_RATE = 2
    
    def __init__(self, name, type):
        if not isinstance(name, str) or not isinstance(type, str):
            raise ValueError("Name and type must be strings.")
        self.name = name
        self.type = type
        self.food_level = random.randrange(55, 80)
        self.water_level = random.randrange(55, 80)
        self.sanitation_level = random.randrange(55, 80)
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

    def get_status(self):
        return {
            "Pet": self.name,
            "Mood": self.get_mood(),
            "Hunger": self.food_level,
            "Thirst": self.water_level,
            "Cleanliness": self.sanitation_level
        }

    def update_status(self):
        time_change = time.time() - self.last_update_time
        rate_of_change = time_change / 1800
        self.food_level = max(self.food_level - rate_of_change * Pet.HUNGER_RATE, 0)
        self.water_level = max(self.water_level - rate_of_change * Pet.THIRST_RATE, 0)
        self.sanitation_level = max(self.sanitation_level - rate_of_change * Pet.CLEANLINESS_RATE, 0)
        self.mood_level = max(self.mood_level - rate_of_change * Pet.MOOD_RATE, 0)
        self.last_update_time = time.time()
    
    def print_status(self):
        status = self.get_status()
        order = ["Pet","Mood","Hunger","Thirst","Cleanliness"]
        for key in order:
            print(key+":",status[key])





    

