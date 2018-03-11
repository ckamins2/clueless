import unittest

from source.server.models.location import Room, Hallway
from source.server.models.character import Character
from source.server.models.player import Player

class TestCharacter(unittest.TestCase):

    def setUp(self):

        # Set up a Player, Location, and Character for all tests
        self.location = Room("Conservatory")
        self.player = Player("SnarkAttack")
        self.character = Character("Professor Plum", self.player, self.location)

        # Add Character to Player and Location
        self.player.set_character(self.character)
        self.location.add_character(self.character)

    def tearDown(self):
        self.location = None
        self.player = None
        self.character = None

    def test_character_initialization(self):
        self.assertEquals(self.character.name, "Professor Plum")
        self.assertEquals(self.player.name, "SnarkAttack")
        self.assertEquals(self.character.location.name, "Conservatory")

    def test_character_in_room(self):
        self.assertTrue(self.character in self.location.characters)


    def test_character_move(self):

        # Second room needed for this test
        new_location = Room("Library")

        self.character.move_character(new_location)

        # Make sure the Character is not in the old Room and is in the new Room
        self.assertFalse(self.location.is_character_in_room(self.character))
        self.assertTrue(new_location.is_character_in_room(self.character))

        # Make sure the Character knows which Room it is in
        self.assertEquals(self.character.location, new_location)