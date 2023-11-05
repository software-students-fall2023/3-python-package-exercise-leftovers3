import pytest
from unittest.mock import patch
from petmagotchi.pet import Pet

TRAVEL_CD_PATCH = 100
TRAVEL_DESTS_PATCH = {
    'park': {
        'res': 'test %s park',
        'stats': {
            'mood_level': 10,
            'sanitation_level': 20,
            'energy_level': 30,
            'food_level': 40,
            'water_level': 50,
        }},
    'hike': {
        'res': 'test %s hike',
        'stats': {
            'mood_level': -10,
            'sanitation_level': -20,
            'energy_level': -30,
            'food_level': -40,
            'water_level': -50,
    }},
}
TRAVEL_ALERTS_PATCH = {
    'mood_level': 'test %s mood_level',
    'sanitation_level': 'test %s sanitation_level',
    'energy_level': 'test %s energy_level',
    'food_level': 'test %s food_level',
    'water_level': 'test %s water_level',
}


# testing pet, patched config
@pytest.fixture
def pet() -> Pet:
    with patch('petmagotchi.pet.Pet.TRAVEL_CD', TRAVEL_CD_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_DESTS', TRAVEL_DESTS_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_ALERTS', TRAVEL_ALERTS_PATCH):
        with patch('time.time', return_value=0):  # create at time 0
            pet0 = Pet('Moana', 'Dog')  # (my dawg 🐕🐕🐶🌊)
        yield pet0


class TestBringTo():

    def test_bring_to_bad_destination(self, pet: Pet):
        with pytest.raises(ValueError):
            pet.bring_to(123)
    
    def test_bring_to_invalid_destination(self, pet: Pet):
        with pytest.raises(Pet.InvalidDestinationError):
            pet.bring_to('movies')

    def test_bring_to_lower(self, pet: Pet):
        assert pet.bring_to('PaRk') == 'test Moana park'

    def test_bring_to_travel_cooldown(self, pet: Pet):
        with patch('time.time', return_value=10):
            assert pet.bring_to('park') == 'test Moana park'
        with patch('time.time', return_value=50):
            assert pet.bring_to('park') == "Moana wants to relax at home. Try waiting some time before bringing them out again!"
        with patch('time.time', return_value=150):
            assert pet.bring_to('hike') == 'test Moana hike'