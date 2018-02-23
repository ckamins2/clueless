import unittest

from source.server.models.location import Location, Room, Hallway

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

    def test_hallway_initialization(self):

        hallway = Hallway("Test hallway")

        self.assertEquals(hallway.name, "Test hallway")
        self.assertEquals(hallway.max_characters, 1)