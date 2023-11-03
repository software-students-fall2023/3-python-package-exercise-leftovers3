import time
import random
from PIL import Image

class Pet:
    class InvalidFoodError(Exception):
        """Raised when an invalid food is given to the pet."""
        pass

    class InvalidQuantityError(Exception):
        """Raised when the user gives too many or too little quantity"""
        
    class InvalidToyError(Exception):
        """Raised when the user gives too many or too little quantity"""
    
    HUNGER_RATE = 3
    THIRST_RATE = 4
    CLEANLINESS_RATE = 1
    MOOD_RATE = 2
    ENERGY_RATE = 2
    VALID_FOODS = {'meat':(15,5),'vegetable':(10,2),'ice cream':(5,15),'bread':(8,8)} #meal:(hunger fiil, mood increase)
    TOYS = {'yarn': 10,'ball':12,'plushie':15,'bone':10} #toy: mood increase
    VALID_TYPES = ["Cat","Dog"]
    
    def __init__(self, name, type):
        if not isinstance(name, str) or not isinstance(type, str):
            raise ValueError("Name and type must be strings.")
        if not isinstance(type, str) or type not in Pet.VALID_TYPES:
            raise ValueError(f"Type must be one of the following: {', '.join(Pet.VALID_TYPES)}.")
        self.name = name
        self.type = type
        self.food_level = random.randint(55, 80)
        self.water_level = random.randint(55, 80)
        self.sanitation_level = random.randint(55, 80)
        self.mood_level = 90
        self.energy_level = random.randint(55, 80)
        self.last_update_time = time.time()
        
        self.favoriteToy = random.choice(list(Pet.TOYS.keys()))

    def get_mood(self):
        if 0 <= self.mood_level < 30:
            return f"{self.name} is upset..."
        elif 30 <= self.mood_level < 80:
            return f"{self.name} is feeling ok..."
        else:
            return f"{self.name} is excited and happy to be with you!"

    def _update_status(self):
        time_change = time.time() - self.last_update_time
        rate_of_change = time_change / 1800
        self.food_level = max(round(self.food_level - rate_of_change * Pet.HUNGER_RATE), 0)
        self.water_level = max(round(self.water_level - rate_of_change * Pet.THIRST_RATE), 0)
        self.sanitation_level = max(round(self.sanitation_level - rate_of_change * Pet.CLEANLINESS_RATE), 0)
        self.mood_level = max(round(self.mood_level - rate_of_change * Pet.MOOD_RATE), 0)
        self.energy_level = min(round(self.energy_level + rate_of_change * Pet.ENERGY_RATE), 100)
        self.last_update_time = time.time()

    def get_status(self):
        self._update_status()
        return {
            "Pet": self.name,
            "Mood": self.get_mood(),
            "Hunger": self.food_level,
            "Thirst": self.water_level,
            "Energy": self.energy_level,
            "Cleanliness": self.sanitation_level,
            "Favorite Toy": self.favoriteToy
        }
    
    def print_status(self):
        status = self.get_status()
        order = ["Pet","Mood","Hunger","Thirst","Energy","Cleanliness", "Favorite Toy"]
        for key in order:
            print(key+":",status[key])

    def feed_pet(self,food,quantity):
        self._update_status()
        if not isinstance(food,str) or not isinstance(quantity,int):
            raise ValueError("Food must be a string and quantity must be an int.")
        if food not in Pet.VALID_FOODS:
            raise Pet.InvalidFoodError(f"'{food}' is not a valid food. Valid foods are: {', '.join(Pet.VALID_FOODS)}")
        if quantity>3 or quantity<1:
            raise Pet.InvalidQuantityError(f"'{quantity}' is not a valid quantity. Valid quantities are 1,2 and 3. Can't give your pet a stomachache!")
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

    def play(self, toy):
        self._update_status()
        if not isinstance(toy, str):
            raise ValueError("Toy must be a string.")
        if toy not in Pet.TOYS:
            raise Pet.InvalidToyError(f"'{toy}' is not a valid toy. Valid toys are: {', '.join(Pet.TOYS)}")
        
        reationStr = ""
        if self.energy_level < 10:
            print(f"{self.name} is too tired to play. Lets give them a break!")
            return
        else:
            energy_decrease = 10
            mood_increase = Pet.TOYS[toy]
            if(self.favoriteToy == toy):
                mood_increase *= 2
                reationStr += f"{self.name} loved playing with their favorite toy! "

            if(random.randint(0,9) == 0): #10% chance of doubling the mood increase
                mood_increase *= 2
                reationStr += f"{self.name} had extra fun playing with you this time! "
            else:
                reationStr += f"{self.name} had fun playing with you! "
            self.mood_level = min(self.mood_level + mood_increase, 100)
            self.energy_level = max(self.energy_level - energy_decrease, 0)
        print(reationStr + "They can't wait to play again!")
          
    def wash(self):
        self._update_status()
        if self.sanitation_level == 100:
            print(f"{self.name} is really clean! No need to wash them.")
        else:
            self.sanitation_level = 100
            print(f"{self.name} is squeaky clean now!")
    
    def pet(self):
        self._update_status()
        
        reationStr = ""
        if self.mood_level < 30:
            print(f"{self.name} is too upset to be pet. Try playing with them!")
            return
        else:
            mood_increase = 5
            if(random.randint(0,9) == 0): #10% chance of doubling the mood increase
                mood_increase *= 2
                reationStr = f"{self.name} is really happy to be pet by you!"
            else:
                reationStr = f"{self.name} enjoyed being pet!"
        self.mood_level = min(self.mood_level + mood_increase, 100)
        print(reationStr)
    
    #TODO: unit test
    def _get_image(self, mood):
        imgAddress = "src/images/"
        if(self.type == "Cat"):
            imgAddress += "cat/cat_"
        elif(self.type == "Dog"):
            imgAddress += "dog/dog_"
        
        if mood == "upset":
            imgAddress += "upset"
        elif mood == "neutral":
            imgAddress += "neutral"
        else:
            imgAddress += "happy"
        
        imgAddress += ".png"
        return Image.open(imgAddress)
    
    #TODO: unit test
    def see_pet(self):
        print(f"Here's what {self.name} looks like right now:")
        if 0 <= self.mood_level < 30:
            return self._get_image("upset").show()
        elif 30 <= self.mood_level < 80:
            return self._get_image("neutral").show()
        else:
            return self._get_image("happy").show()

