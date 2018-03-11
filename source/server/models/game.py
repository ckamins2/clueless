from source.server.models.location import Room, Hallway, StartRoom
from source.server.models.player import Player


class Game(object):
    players = None
    map = None

    def __init__(self):
        if self.players is None:
            self.players = []

        if self.map is None:
            self.map = []

    def initialize_board(self):

        # Initialize rooms
        study = Room("Study")
        hall = Room("Hall")
        lounge = Room("Lounge")
        library = Room("Library")
        billiard_room = Room("Billiard Room")
        dining_room = Room("Dining Room")
        conservatory = Room("Conservatory")
        ballroom = Room("Ballroom")
        kitchen = Room("Kitchen")

        # Initialize hallways
        study_hall_hallway = Hallway("Study - Hall Hallway")
        hall_lounge_hallway = Hallway("Hall - Lounge Hallway")
        study_library_hallway = Hallway("Study - Library Hallway")
        hall_billiard_room_hallway = Hallway("Hall - Billiard Room Hallway")
        lounge_dining_room_hallway = Hallway("Lounge - Dining Room Hallway")
        library_billiard_room_hallway = Hallway("Library - Billiard Room Hallway")
        billiard_room_dining_room_hallway = Hallway("Billiard Room - Dining Room Hallway")
        library_conservatory_hallway = Hallway("Library - Conservatory Hallway")
        billiard_room_ballroom_hallway = Hallway("Billiard Room - Ballroom Hallway")
        dining_room_kitchen_hallway = Hallway("Dining Room - Kitchen Hallway")
        conservatory_ballroom_hallway = Hallway("Conservatory - Ballroom Hallway")
        ballroom_kitchen_hallway = Hallway("Ballroom - Kitchen Hallway")

        # Initialize start rooms
        # TODO: Add characters to these starting rooms

        scarlet_start = StartRoom()
        plum_start = StartRoom()
        mustard_start = StartRoom()
        peacock_start = StartRoom()
        green_start = StartRoom()
        white_start = StartRoom()


        # Add relationships for all rooms
        study.add_adjacent_locations([study_hall_hallway, study_library_hallway, kitchen], ['E', 'S', 'secret'])
        hall.add_adjacent_locations([study_hall_hallway, hall_lounge_hallway, hall_billiard_room_hallway], ['W', 'E', 'S'])
        lounge.add_adjacent_locations([hall_lounge_hallway, lounge_dining_room_hallway, conservatory], ['W', 'S', 'secret'])
        library.add_adjacent_locations([study_library_hallway, library_billiard_room_hallway, library_conservatory_hallway], ['N', 'E', 'S'])
        billiard_room.add_adjacent_locations([hall_billiard_room_hallway, library_billiard_room_hallway, billiard_room_dining_room_hallway, billiard_room_ballroom_hallway], ['N', 'W', 'E', 'S'])
        dining_room.add_adjacent_locations([lounge_dining_room_hallway, billiard_room_dining_room_hallway, dining_room_kitchen_hallway], ['N', 'W', 'S'])
        conservatory.add_adjacent_locations([library_conservatory_hallway, conservatory_ballroom_hallway, lounge], ['N', 'E', 'secret'])
        ballroom.add_adjacent_locations([billiard_room_ballroom_hallway, conservatory_ballroom_hallway, ballroom_kitchen_hallway], ['N', 'W', 'E'])
        kitchen.add_adjacent_locations([dining_room_kitchen_hallway, ballroom_kitchen_hallway, study], ['N', 'W', 'secret'])

        # Add relationships for all hallways
        study_hall_hallway.add_adjacent_locations([study, hall], ['W', 'E'])
        hall_lounge_hallway.add_adjacent_locations([hall, lounge], ['W', 'E'])
        study_library_hallway.add_adjacent_locations([study, library], ['N', 'S'])
        hall_billiard_room_hallway.add_adjacent_locations([hall, billiard_room], ['N', 'S'])
        lounge_dining_room_hallway.add_adjacent_locations([lounge, dining_room], ['N', 'S'])
        library_billiard_room_hallway.add_adjacent_locations([library, billiard_room], ['W', 'E'])
        billiard_room_dining_room_hallway.add_adjacent_locations([billiard_room, dining_room], ['W', 'E'])
        library_conservatory_hallway.add_adjacent_locations([library, conservatory], ['N', 'S'])
        billiard_room_ballroom_hallway.add_adjacent_locations([billiard_room, ballroom], ['N', 'S'])
        dining_room_kitchen_hallway.add_adjacent_locations([dining_room, kitchen], ['N', 'S'])
        conservatory_ballroom_hallway.add_adjacent_locations([conservatory, ballroom], ['W', 'E'])
        ballroom_kitchen_hallway.add_adjacent_locations([ballroom, kitchen], ['W', 'E'])

        #Add relationships for StartRooms
        scarlet_start.add_adjacent_location(hall_lounge_hallway, 'S')
        plum_start.add_adjacent_location(study_library_hallway, 'E')
        mustard_start.add_adjacent_location(lounge_dining_room_hallway, 'W')
        peacock_start.add_adjacent_location(library_conservatory_hallway, 'E')
        green_start.add_adjacent_location(conservatory_ballroom_hallway, 'N')
        white_start.add_adjacent_location(ballroom_kitchen_hallway, 'N')

        # TODO: Fingure out what rooms we actually want to rmemeber, I think we really only need one
        self.map.append(study)

