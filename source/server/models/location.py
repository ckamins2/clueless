from abc import ABCMeta, abstractmethod

class Location():
    __metaclass__ = ABCMeta
    name = ""
    adjacent_locations = {'N': None, 'E': None, 'S': None, 'W': None}
    characters = []
    max_characters = 0

    @abstractmethod
    def __init__(self, name, adjacent_locations = []):
        self.name = name

    def __str__(self):
        return self.name

    def get_characters(self):
        return self.characters

    def add_adjacent_location(self, location, direction):
        self.adjacent_locations[direction] = location

    # Locations and directions must be passed in in corresponding order
    def add_adjacent_locations(self, locations, directions):
        for idx, location in enumerate(locations):
            self.add_adjacent_location(location, directions[idx])

    def is_valid_move_target(self):
        return (len(self.characters) < self.max_characters)

    def get_valid_moves(self):
        directions = []
        for direction, location in self.adjacent_locations.iter_items():
            if(location.is_valid_move_target()):
                directions.append((location, direction))

    def move_character_into_location(self, character):
        self.characters.append(character)


class Room(Location):

    def __init__(self, name, adjacent_locations = []):
        super(Room, self).__init__(name, adjacent_locations)
        self.max_characters = 6

class Hallway(Location):

    def __init__(self, name, adjacent_locations = []):
        super(Hallway, self).__init__(name, adjacent_locations)
        self.max_characters = 1
