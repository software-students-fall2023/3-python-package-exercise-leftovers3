import pytest
from petmagotchi.pet import Pet
from unittest.mock import patch

class TestPet:
    def setup_method(self):
        self.pet = Pet(name="Yuka", type="Cat")
    
    def test_pet_creation(self):
        assert isinstance(self.pet.name,str)
        assert isinstance(self.pet.type,str)
        assert 55 <= self.pet.food_level <= 80
        assert 55 <= self.pet.water_level <= 80
        assert 55 <= self.pet.sanitation_level <= 80
        assert self.pet.mood_level == 90
    
    def test_mood_status(self):
        self.pet.mood_level = 10
        assert self.pet.get_mood() == f"{self.pet.name} is sad and lonely..."
        
        self.pet.mood_level = 30
        assert self.pet.get_mood() == f"{self.pet.name} is sad..."

        self.pet.mood_level = 50
        assert self.pet.get_mood() == f"{self.pet.name} would like some more attention..."

        self.pet.mood_level = 70
        assert self.pet.get_mood() == f"{self.pet.name} is happy!"

        self.pet.mood_level = 90
        assert self.pet.get_mood() == f"{self.pet.name} is excited and happy to be with you!"
    
    def test_update_status_time_shift(self):
        starting_time = 0
        jump = 3600
        with patch('time.time', return_value = starting_time):
            pet = Pet(name="Yuka", type="Cat")
            inital_status = pet.get_status()
        
        with patch('time.time', return_value = starting_time + jump):
            updated_status = pet.get_status()
        
        assert updated_status["Hunger"] < inital_status["Hunger"]
        assert updated_status["Thirst"] < inital_status["Thirst"]
        assert updated_status["Cleanliness"] < inital_status["Cleanliness"]

        