import unittest

from source.server.models.location import Room, Hallway
from source.server.models.game import Game
from source.server.models.player import Player

class TestGame(unittest.TestCase):

    def setUp(self):

        # Set up a Player, Location, and Character for all tests
        self.game = Game()
        self.game.initialize_board()

    def tearDown(self):
        self.game = None

    # This is a really long test, but if something in here ever doesn't work
    # we'll be really glad to ahve this one
    def test_game_board_initialization(self):


        # Build up a full map using relations

        study = self.game.map.pop()
        study_hall_hallway = study.adjacent_locations['E']
        study_library_hallway = study.adjacent_locations['S']

        hall = study_hall_hallway.adjacent_locations['E']
        library = study_library_hallway.adjacent_locations['S']

        hall_lounge_hallway = hall.adjacent_locations['E']
        hall_billiard_room_hallway = hall.adjacent_locations['S']

        library_billiard_room_hallway = library.adjacent_locations['E']
        library_conservatory_hallway = library.adjacent_locations['S']

        lounge = hall_lounge_hallway.adjacent_locations['E']
        billiard_room = hall_billiard_room_hallway.adjacent_locations['S']
        conservatory = library_conservatory_hallway.adjacent_locations['S']

        lounge_dining_room_hallway = lounge.adjacent_locations['S']
        billiard_room_ballroom_hallway = billiard_room.adjacent_locations['S']
        billiard_room_dining_room_hallway = billiard_room.adjacent_locations['E']

        conservatory_ballroom_hallway = conservatory.adjacent_locations['E']

        dining_room = lounge_dining_room_hallway.adjacent_locations['S']
        ballroom = billiard_room_ballroom_hallway.adjacent_locations['S']

        dining_room_kitchen_hallway = dining_room.adjacent_locations['S']
        ballroom_kitchen_hallway = ballroom.adjacent_locations['E']

        kitchen = ballroom_kitchen_hallway.adjacent_locations['E']

        # Test all rooms from correct relationships

        # Note: Tests will fail whether or not the check is against None
        # (if checking None and a room is there equality will be off, if
        # checking a name and there is no room we'll throw an error)

        # Study
        self.assertEquals(study.name, "Study")
        self.assertEquals(study.north(), None)
        self.assertEquals(study.south().name, "Study - Library Hallway")
        self.assertEquals(study.east().name, "Study - Hall Hallway")
        self.assertEquals(study.west(), None)
        self.assertEquals(study.secret().name, "Kitchen")

        # Hall
        self.assertEquals(hall.name, "Hall")
        self.assertEquals(study.north(), None)
        self.assertEquals(hall.adjacent_locations['S'].name, "Hall - Billiard Room Hallway")
        self.assertEquals(hall.adjacent_locations['E'].name, "Hall - Lounge Hallway")
        self.assertEquals(hall.adjacent_locations['W'].name, "Study - Hall Hallway")
        self.assertEquals(hall.secret(), None)

        # Lounge
        self.assertEquals(lounge.name, "Lounge")
        self.assertEquals(lounge.north(), None)
        self.assertEquals(lounge.south().name, "Lounge - Dining Room Hallway")
        self.assertEquals(lounge.east(), None)
        self.assertEquals(lounge.west().name, "Hall - Lounge Hallway")
        self.assertEquals(lounge.secret().name, "Conservatory")

        # Library
        self.assertEquals(library.name, "Library")
        self.assertEquals(library.north().name, "Study - Library Hallway")
        self.assertEquals(library.south().name, "Library - Conservatory Hallway")
        self.assertEquals(library.east().name, "Library - Billiard Room Hallway")
        self.assertEquals(library.west(), None)
        self.assertEquals(library.secret(), None)

        # Billiard Room
        self.assertEquals(billiard_room.name, "Billiard Room")
        self.assertEquals(billiard_room.north().name, "Hall - Billiard Room Hallway")
        self.assertEquals(billiard_room.south().name, "Billiard Room - Ballroom Hallway")
        self.assertEquals(billiard_room.east().name, "Billiard Room - Dining Room Hallway")
        self.assertEquals(billiard_room.west().name, "Library - Billiard Room Hallway")
        self.assertEquals(billiard_room.secret(), None)

        # Dining Room
        self.assertEquals(dining_room.name, "Dining Room")
        self.assertEquals(dining_room.north().name, "Lounge - Dining Room Hallway")
        self.assertEquals(dining_room.south().name, "Dining Room - Kitchen Hallway")
        self.assertEquals(dining_room.east(), None)
        self.assertEquals(dining_room.west().name, "Billiard Room - Dining Room Hallway")
        self.assertEquals(dining_room.secret(), None)

        # Conservatory
        self.assertEquals(conservatory.name, "Conservatory")
        self.assertEquals(conservatory.north().name, "Library - Conservatory Hallway")
        self.assertEquals(conservatory.south(), None)
        self.assertEquals(conservatory.east().name, "Conservatory - Ballroom Hallway")
        self.assertEquals(conservatory.west(), None)
        self.assertEquals(conservatory.secret().name, "Lounge")

        # Ballroom
        self.assertEquals(ballroom.name, "Ballroom")
        self.assertEquals(ballroom.north().name, "Billiard Room - Ballroom Hallway")
        self.assertEquals(ballroom.south(), None)
        self.assertEquals(ballroom.east().name, "Ballroom - Kitchen Hallway")
        self.assertEquals(ballroom.west().name, "Conservatory - Ballroom Hallway")
        self.assertEquals(ballroom.secret(), None)

        # Kitchen
        self.assertEquals(kitchen.name, "Kitchen")
        self.assertEquals(kitchen.north().name, "Dining Room - Kitchen Hallway")
        self.assertEquals(kitchen.south(), None)
        self.assertEquals(kitchen.east(), None)
        self.assertEquals(kitchen.west().name, "Ballroom - Kitchen Hallway")
        self.assertEquals(kitchen.secret().name, "Study")


        # Check all hallway connections

        # Study - Hall hallway
        self.assertEquals(study_hall_hallway.name, "Study - Hall Hallway")
        self.assertEquals(study_hall_hallway.north(), None)
        self.assertEquals(study_hall_hallway.south(), None)
        self.assertEquals(study_hall_hallway.east().name, "Hall")
        self.assertEquals(study_hall_hallway.west().name, "Study")
        self.assertEquals(study_hall_hallway.secret(), None)

        # Hall - Lounge hallway
        self.assertEquals(hall_lounge_hallway.name, "Hall - Lounge Hallway")
        self.assertEquals(hall_lounge_hallway.north(), None)
        self.assertEquals(hall_lounge_hallway.south(), None)
        self.assertEquals(hall_lounge_hallway.east().name, "Lounge")
        self.assertEquals(hall_lounge_hallway.west().name, "Hall")
        self.assertEquals(hall_lounge_hallway.secret(), None)

        # Study - Library hallway
        self.assertEquals(study_library_hallway.name, "Study - Library Hallway")
        self.assertEquals(study_library_hallway.north().name, "Study")
        self.assertEquals(study_library_hallway.south().name, "Library")
        self.assertEquals(study_library_hallway.east(), None)
        self.assertEquals(study_library_hallway.west(), None)
        self.assertEquals(study_library_hallway.secret(), None)

        # Hall - Billiard Room hallway
        self.assertEquals(hall_billiard_room_hallway.name, "Hall - Billiard Room Hallway")
        self.assertEquals(hall_billiard_room_hallway.north().name, "Hall")
        self.assertEquals(hall_billiard_room_hallway.south().name, "Billiard Room")
        self.assertEquals(hall_billiard_room_hallway.east(), None)
        self.assertEquals(hall_billiard_room_hallway.west(), None)
        self.assertEquals(hall_billiard_room_hallway.secret(), None)

        # Lounge - Dining Room Hallway
        self.assertEquals(lounge_dining_room_hallway.name, "Lounge - Dining Room Hallway")
        self.assertEquals(lounge_dining_room_hallway.north().name, "Lounge")
        self.assertEquals(lounge_dining_room_hallway.south().name, "Dining Room")
        self.assertEquals(lounge_dining_room_hallway.east(), None)
        self.assertEquals(lounge_dining_room_hallway.west(), None)
        self.assertEquals(lounge_dining_room_hallway.secret(), None)

        # Library - Billiard Room Hallway
        self.assertEquals(library_billiard_room_hallway.name, "Library - Billiard Room Hallway")
        self.assertEquals(library_billiard_room_hallway.north(), None)
        self.assertEquals(library_billiard_room_hallway.south(), None)
        self.assertEquals(library_billiard_room_hallway.east().name, "Billiard Room")
        self.assertEquals(library_billiard_room_hallway.west().name, "Library")
        self.assertEquals(library_billiard_room_hallway.secret(), None)

        # Billiard Room - Dining Room Hallway
        self.assertEquals(billiard_room_dining_room_hallway.name, "Billiard Room - Dining Room Hallway")
        self.assertEquals(billiard_room_dining_room_hallway.north(), None)
        self.assertEquals(billiard_room_dining_room_hallway.south(), None)
        self.assertEquals(billiard_room_dining_room_hallway.east().name, "Dining Room")
        self.assertEquals(billiard_room_dining_room_hallway.west().name, "Billiard Room")
        self.assertEquals(billiard_room_dining_room_hallway.secret(), None)

        # Library - Conservatory Hallway
        self.assertEquals(library_conservatory_hallway.name, "Library - Conservatory Hallway")
        self.assertEquals(library_conservatory_hallway.north().name, "Library")
        self.assertEquals(library_conservatory_hallway.south().name, "Conservatory")
        self.assertEquals(library_conservatory_hallway.east(), None)
        self.assertEquals(library_conservatory_hallway.west(), None)
        self.assertEquals(library_conservatory_hallway.secret(), None)

        # Billiard Room - Ballroom Hallway
        self.assertEquals(billiard_room_ballroom_hallway.name, "Billiard Room - Ballroom Hallway")
        self.assertEquals(billiard_room_ballroom_hallway.north().name, "Billiard Room")
        self.assertEquals(billiard_room_ballroom_hallway.south().name, "Ballroom")
        self.assertEquals(billiard_room_ballroom_hallway.east(), None)
        self.assertEquals(billiard_room_ballroom_hallway.west(), None)
        self.assertEquals(billiard_room_ballroom_hallway.secret(), None)

        # Dining Room - Kitchen Hallway
        self.assertEquals(dining_room_kitchen_hallway.name, "Dining Room - Kitchen Hallway")
        self.assertEquals(dining_room_kitchen_hallway.north().name, "Dining Room")
        self.assertEquals(dining_room_kitchen_hallway.south().name, "Kitchen")
        self.assertEquals(dining_room_kitchen_hallway.east(), None)
        self.assertEquals(dining_room_kitchen_hallway.west(), None)
        self.assertEquals(dining_room_kitchen_hallway.secret(), None)

        # Conservatory - Ballroom Hallway
        self.assertEquals(conservatory_ballroom_hallway.name, "Conservatory - Ballroom Hallway")
        self.assertEquals(conservatory_ballroom_hallway.north(), None)
        self.assertEquals(conservatory_ballroom_hallway.south(), None)
        self.assertEquals(conservatory_ballroom_hallway.east().name, "Ballroom")
        self.assertEquals(conservatory_ballroom_hallway.west().name, "Conservatory")
        self.assertEquals(conservatory_ballroom_hallway.secret(), None)

        # Ballroom - Kitchen Hallway
        self.assertEquals(ballroom_kitchen_hallway.name, "Ballroom - Kitchen Hallway")
        self.assertEquals(ballroom_kitchen_hallway.north(), None)
        self.assertEquals(ballroom_kitchen_hallway.south(), None)
        self.assertEquals(ballroom_kitchen_hallway.east().name, "Kitchen")
        self.assertEquals(ballroom_kitchen_hallway.west().name, "Ballroom")
        self.assertEquals(ballroom_kitchen_hallway.secret(), None)


        # study = Room("Study")
        # hall = Room("Hall")
        # lounge = Room("Lounge")
        # library = Room("Library")
        # billiard_room = Room("Billiard Room")
        # dining_room = Room("Dining Room")
        # conservatory = Room("Conservatory")
        # ballroom = Room("Ballroom")
        # kitchen = Room("Kitchen")
        #
        # study_hall_hallway = Hallway("Study - Hall Hallway")
        # hall_lounge_hallway = Hallway("Hall - Lounge Hallway")
        # study_library_hallway = Hallway("Study - Library Hallway")
        # hall_billiard_room_hallway = Hallway("Hall - Billiard Room Hallway")
        # lounge_dining_room_hallway = Hallway("Lounge - Dining Room Hallway")
        # library_billiard_room_hallway = Hallway("Library - Billiard Room Hallway")
        # billiard_room_dining_room_hallway = Hallway("Billiard Room - Dining Room Hallway")
        # library_conservatory_hallway = Hallway("Library - Conservatory Hallway")
        # billiard_room_ballroom_hallway = Hallway("Billiard Room - Ballroom Hallway")
        # dining_room_kitchen_hallway = Hallway("Dining Room - Kitchen Hallway")
        # conservatory_ballroom_hallway = Hallway("Conservatory - Ballroom Hallway")
        # ballroom_kitchen_hallway = Hallway("Ballroom - Kitchen Hallway")
        #
        # scarlet_start = StartRoom()
        # plum_start = StartRoom()
        # mustard_start = StartRoom()
        # peacock_start = StartRoom()
        # green_start = StartRoom()
        # white_start = StartRoom()