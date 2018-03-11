import unittest

from source.server.models.location import Location, Room, Hallway
from source.server.models.character import Character

class TestLocation(unittest.TestCase):

    def test_location_initialization(self):
        self.assertRaises(TypeError, Location, "Test location")

class TestRoom(unittest.TestCase):

    def setUp(self):
        self.room = Room("Test room")

    def test_room_initialization(self):
        self.assertEquals(self.room.name, "Test room")
        self.assertEqual(self.room.max_characters, 6)


class TestHallway(unittest.TestCase):

    def setUp(self):
        self.hallway = Hallway("Test hallway")

    def test_hallway_initialization(self):
        self.assertEquals(self.hallway.name, "Test hallway")
        self.assertEquals(self.hallway.max_characters, 1)

class TestHallwaysMaxCharacterLimit(unittest.TestCase):

    def setUp(self):
        self.start_room = Room("Test room")
        self.hallway = Hallway("Test Hallway")

        self.character1 = Character("Character1", None, self.start_room)
        self.character2 = Character("Character2", None, self.start_room)

        self.start_room.add_character(self.character1)
        self.start_room.add_character(self.character2)

    def test_no_more_than_one_in_hallway(self):

        # Sanity checks
        self.assertEquals(len(self.start_room.characters), 2)
        self.assertEquals(len(self.hallway.characters), 0)

        # Check that we can move first person into hallway
        self.assertTrue(self.hallway.is_valid_move_target())

        if self.hallway.is_valid_move_target():
            self.character1.move_character(self.hallway)

        # Check that character1 moved properly
        self.assertEquals(len(self.start_room.characters), 1)
        self.assertEquals(len(self.hallway.characters), 1)

        self.assertTrue(self.hallway.is_character_in_room(self.character1))

        # Check that hallways can no longer be moved into
        self.assertFalse(self.hallway.is_valid_move_target())

        # This should not be true
        if self.hallway.is_valid_move_target():
            self.character1.move_character(self.hallway)
            self.fail("Should not have been able to move second person into hallway")

        # Confirm that character2 did not move
        self.assertEquals(len(self.start_room.characters), 1)
        self.assertEquals(len(self.hallway.characters), 1)
