from abc import ABCMeta, abstractmethod

class Location():
    __metaclass__ = ABCMeta
    name = ""
    adjacent_locations = None
    characters = None
    max_characters = 0

    @abstractmethod
    def __init__(self, name):
        self.name = name
        if self.characters is None:
            self.characters = []
        if self.adjacent_locations is None:
            self.adjacent_locations = {}

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

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def is_character_in_room(self, character):
        return character in self.characters

    def north(self):
        return self.adjacent_locations.get('N', None)

    def south(self):
        return self.adjacent_locations.get('S', None)

    def east(self):
        return self.adjacent_locations.get('E', None)

    def west(self):
        return self.adjacent_locations.get('W', None)

    def secret(self):
        return self.adjacent_locations.get('secret', None)


class Room(Location):

    def __init__(self, name):
        super(Room, self).__init__(name)
        self.max_characters = 6

class Hallway(Location):

    def __init__(self, name,):
        super(Hallway, self).__init__(name)
        self.max_characters = 1

class StartRoom(Location):

    def __init__(self):
        super(StartRoom, self).__init__("")
        # Setting this to zero because no one should ever
        # move into this room
        self.max_characters = 0
