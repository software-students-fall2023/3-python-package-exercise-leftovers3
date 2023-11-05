import pytest
from unittest.mock import patch
from petmagotchi.pet import Pet

TRAVEL_CD_PATCH = 60*60  # one hour between trips
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


# testing pet
@pytest.fixture
def pet() -> Pet:
    yield Pet('Moana', 'Dog')  # (my dawg 🐕🐕🐶🌊)

# testing pet, patched config
@pytest.fixture
def patch_pet(pet: Pet) -> Pet:
    with patch('petmagotchi.pet.Pet.TRAVEL_CD', TRAVEL_CD_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_DESTS', TRAVEL_DESTS_PATCH),\
    patch('petmagotchi.pet.Pet.TRAVEL_ALERTS', TRAVEL_ALERTS_PATCH):
        yield pet


class TestBringTo():

    def test_bring_to_bad_destination(self, pet: Pet):
        with pytest.raises(ValueError):
            pet.bring_to(123)
    
    def test_bring_to_invalid_destination(self, patch_pet: Pet):
        with pytest.raises(Pet.InvalidDestinationError):
            assert patch_pet.bring_to('MovIEs')