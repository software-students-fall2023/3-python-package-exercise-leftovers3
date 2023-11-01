import pytest
import random
from io import StringIO
from petmagotchi.pet import Pet
from unittest.mock import patch

class TestPet:
    def setup_method(self):
        self.pet = Pet(name="Yuka", type="Cat")
    
    #tests constructor
    def test_pet_creation(self):
        assert isinstance(self.pet.name,str)
        assert isinstance(self.pet.type,str)
        assert 55 <= self.pet.food_level <= 80
        assert 55 <= self.pet.water_level <= 80
        assert 55 <= self.pet.sanitation_level <= 80
        assert self.pet.mood_level == 90

    def test_invalid_pet_creation(self):
        with pytest.raises(ValueError):
            Pet(name=123,type="Cat")
        with pytest.raises(ValueError):
            Pet(name="Yuka",type=123)
    
    def test_pet_creation_boundary_values(self):
        pets = [Pet(name="Test",type="Type") for _ in range(1000)]
        food_levels = [pet.food_level for pet in pets]
        water_levels = [pet.water_level for pet in pets]
        sanitation_levels = [pet.sanitation_level for pet in pets]
        mood_levels = [pet.mood_level for pet in pets]
        assert min(food_levels) == 55
        assert max(food_levels) == 80 
        assert min(water_levels) == 55
        assert max(water_levels) == 80
        assert min(sanitation_levels) == 55
        assert max(sanitation_levels) == 80
        assert min(mood_levels) == 90
        assert max(mood_levels) == 90
    
    #tests get_mood
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

    def test_mood_boundaries(self):
        boundaries = [0, 19, 20, 39, 40, 59, 60, 79, 80, 100]
        expected_responses = [
            f"{self.pet.name} is sad and lonely...",
            f"{self.pet.name} is sad and lonely...",
            f"{self.pet.name} is sad...",
            f"{self.pet.name} is sad...",
            f"{self.pet.name} would like some more attention...",
            f"{self.pet.name} would like some more attention...",
            f"{self.pet.name} is happy!",
            f"{self.pet.name} is happy!",
            f"{self.pet.name} is excited and happy to be with you!",
            f"{self.pet.name} is excited and happy to be with you!"
        ]
        for i, boundary in enumerate(boundaries):
            self.pet.mood_level = boundary
            assert self.pet.get_mood() == expected_responses[i]
    
    def test_randomized_mood_status(self):
        mood_ranges = {
            (0, 19): f"{self.pet.name} is sad and lonely...",
            (20, 39): f"{self.pet.name} is sad...",
            (40, 59): f"{self.pet.name} would like some more attention...",
            (60, 79): f"{self.pet.name} is happy!",
            (80, 100): f"{self.pet.name} is excited and happy to be with you!"
        }

        for mood_range, expected_mood in mood_ranges.items():
            for i in range(1000):
                random_mood = random.randint(mood_range[0], mood_range[1])
                self.pet.mood_level = random_mood
                assert self.pet.get_mood() == expected_mood


    #Test get_updated_status
    def test_update_status_value_decrease(self):
        starting_time = 0
        jump = 3600
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")
            initial_status = self.pet.get_updated_status()
            initial_food = self.pet.food_level
            initial_water = self.pet.water_level
            initial_sanitation = self.pet.sanitation_level
            initial_mood = self.pet.mood_level

        with patch('time.time', return_value=starting_time + jump):
            updated_status = self.pet.get_updated_status()
            updated_food = self.pet.food_level
            updated_water = self.pet.water_level
            updated_sanitation = self.pet.sanitation_level
            updated_mood = self.pet.mood_level

        assert updated_food < initial_food
        assert updated_water < initial_water
        assert updated_sanitation < initial_sanitation
        assert updated_mood < initial_mood
        assert updated_status["Hunger"] < initial_status["Hunger"]
        assert updated_status["Thirst"] < initial_status["Thirst"]
        assert updated_status["Cleanliness"] < initial_status["Cleanliness"]
        

    def test_exact_status_update_values(self):
        starting_time = 0
        jump = 3600  # 1 hour
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")
            initial_food = self.pet.food_level
            initial_water = self.pet.water_level
            initial_sanitation = self.pet.sanitation_level
            initial_mood = self.pet.mood_level

        expected_food_change = (jump/1800) * Pet.HUNGER_RATE
        expected_water_change = (jump/1800) * Pet.THIRST_RATE
        expected_sanitation_change = (jump/1800) * Pet.CLEANLINESS_RATE
        expected_mood_change = (jump/1800) * Pet.MOOD_RATE

        with patch('time.time', return_value=starting_time + jump):
            updated_status = self.pet.get_updated_status()

        assert self.pet.food_level == max(initial_food - expected_food_change, 0)
        assert self.pet.water_level == max(initial_water - expected_water_change, 0)
        assert self.pet.sanitation_level == max(initial_sanitation - expected_sanitation_change, 0)
        assert self.pet.mood_level == max(initial_mood - expected_mood_change, 0)
        assert updated_status["Hunger"] == max(initial_food - expected_food_change, 0)
        assert updated_status["Thirst"] == max(initial_water - expected_water_change, 0)
        assert updated_status["Cleanliness"] == max(initial_sanitation - expected_sanitation_change, 0)

    def test_minimum_status_values_after_large_time_jump(self):
        starting_time = 0
        large_jump = 10000000
        with patch('time.time', return_value=starting_time):
            self.pet = Pet(name="Yuka", type="Cat")

        with patch('time.time', return_value=starting_time + large_jump):
            updated_status = self.pet.get_updated_status()
            updated_mood = self.pet.mood_level

        assert updated_status["Hunger"] == 0
        assert updated_status["Thirst"] == 0
        assert updated_status["Cleanliness"] == 0
        assert self.pet.mood_level == 0
        assert updated_status["Mood"] == f"{self.pet.name} is sad and lonely..."

    #test print status
    def test_print_status(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.pet.print_status()
            output = mock_stdout.getvalue()

        lines = output.strip().split("\n")

        expected_output = [
            "Pet: Yuka",
            f"Mood: {self.pet.get_updated_status()['Mood']}",
            f"Hunger: {self.pet.get_updated_status()['Hunger']}",
            f"Thirst: {self.pet.get_updated_status()['Thirst']}",
            f"Cleanliness: {self.pet.get_updated_status()['Cleanliness']}"
        ]

        for i in range(len(lines)):
            assert lines[i] == expected_output[i]


        