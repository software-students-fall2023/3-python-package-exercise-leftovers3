import unittest
from unittest.mock import patch
from src.petmagotchi.pet import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.petCat = Pet(name="MeowMeow", type="Cat")
        self.petDog = Pet(name="BarkBark", type="Dog")
    
    # test image open cat
    
    # test image open dog
    