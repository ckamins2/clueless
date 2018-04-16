# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from random import shuffle

# Create your models here.

class Game(models.Model):
    players = models.ManyToManyField('Player')
    game_map = models.ForeignKey('Map', null=True)
    case_file = models.ManyToManyField('Card')
    characters = models.ManyToManyField('Character')

    @classmethod
    def create(cls):
        game = cls()
        game.save()
        game.createCharacters()
        return game

    @classmethod
    def get_current_game(cls):
        return Game.objects.order_by('-id')[:1].get()

    def __str__(self):
        return str(self.id)

    def get_current_game_players(self):
        return Game.get_current_game().players.all()

    def get_current_player(self, username):
        try:
            return self.get_current_game_players().get(username=username)
        except Player.DoesNotExist:
            return None

    def get_characters(self):
        print self.characters.all()
        return self.characters.all()

    def createCharacters(self):
        col_mustard = Character.create('Colonel Mustard')
        miss_scarlet = Character.create('Miss Scarlet')
        prof_plum = Character.create('Professor Plum')
        mr_green = Character.create('Mr. Green')
        mrs_white = Character.create('Mrs. White')
        mrs_peacock = Character.create('Mrs. Peacock')

        col_mustard.save()
        miss_scarlet.save()
        prof_plum.save()
        mr_green.save()
        mrs_white.save()
        mrs_peacock.save()

        self.characters.add(col_mustard)
        self.characters.add(miss_scarlet)
        self.characters.add(prof_plum)
        self.characters.add(mr_green)
        self.characters.add(mrs_white)
        self.characters.add(mrs_peacock)

        self.save()

    def initialize_game(self):
        cards = self.initialize_cards()
        print "Cards initialized"
        print cards
        cards = self.shuffle_cards(cards)
        print "Cards shuffled"
        cards = self.get_case_file(cards)
        self.pass_out_cards(cards)


    def initialize_cards(self):
        col_mustard = Card.create('Colonel Mustard', 'suspect')
        miss_scarlet = Card.create('Miss Scarlet', 'suspect')
        prof_plum = Card.create('Professor Plum', 'suspect')
        mr_green = Card.create('Mr. Green', 'suspect')
        mrs_white = Card.create('Mrs. White', 'suspect')
        mrs_peacock = Card.create('Mrs. Peacock', 'suspect')

        rope = Card.create('Rope', 'weapon')
        lead_pipe = Card.create('Lead Pipe', 'weapon')
        knife = Card.create('Knife', 'weapon')
        wrench = Card.create('Wrench', 'weapon')
        candlestick = Card.create('Candlestick', 'weapon')
        revolver = Card.create('Revolver', 'weapon')

        study = Card.create("Study", 'room')
        hall = Card.create("Hall", 'room')
        lounge = Card.create("Lounge", 'room')
        library = Card.create("Library", 'room')
        billiard_room = Card.create("Billiard Room", 'room')
        dining_room = Card.create("Dining Room", 'room')
        conservatory = Card.create("Conservatory", 'room')
        ballroom = Card.create("Ballroom", 'room')
        kitchen = Card.create("Kitchen", 'room')

        col_mustard.save()
        miss_scarlet.save()
        prof_plum.save()
        mr_green.save()
        mrs_white.save()
        mrs_peacock.save()

        rope.save()
        lead_pipe.save()
        knife.save()
        wrench.save()
        candlestick.save()
        revolver.save()

        study.save()
        hall.save()
        lounge.save()
        library.save()
        billiard_room.save()
        dining_room.save()
        conservatory.save()
        ballroom.save()
        kitchen.save()

        cards = []

        cards.append(col_mustard)
        cards.append(miss_scarlet)
        cards.append(prof_plum)
        cards.append(mr_green)
        cards.append(mrs_white)
        cards.append(mrs_peacock)

        cards.append(rope)
        cards.append(lead_pipe)
        cards.append(knife)
        cards.append(wrench)
        cards.append(candlestick)
        cards.append(revolver)

        cards.append(study)
        cards.append(hall)
        cards.append(lounge)
        cards.append(library)
        cards.append(billiard_room)
        cards.append(dining_room)
        cards.append(conservatory)
        cards.append(ballroom)
        cards.append(kitchen)

        return cards

    def shuffle_cards(self, cards):

        print cards

        shuffle(cards)

        print cards

        return cards

    def get_case_file(self, cards):
        haveSuspect = None
        haveWeapon = None
        haveRoom = None

        print "Get case file"
        print cards

        for card in cards:
            print card.card_type
            if haveWeapon is None and card.card_type == 'weapon':
                self.case_file.add(card)
                haveWeapon = card
                print card.name + " found"
            elif haveSuspect is None and card.card_type == 'suspect':
                self.case_file.add(card)
                haveSuspect = card
                print card.name + " found"
            elif haveRoom is None and card.card_type == 'room':
                self.case_file.add(card)
                haveRoom = card
                print card.name + " found"

        cards.remove(haveSuspect)
        cards.remove(haveWeapon)
        cards.remove(haveRoom)

        print cards

        self.save()

        return cards

    def pass_out_cards(self, cards):

        num_players = len(self.players.all())

        counter = 0

        if(num_players > 0):
            for player in self.players.all():
                player.hand = [cards[x] for x in range(len(cards)) if x % num_players == counter]
                counter += 1
                player.save()

        for player in self.players.all():
            print player
            print player.hand.all()



class Player(models.Model):
    username = models.CharField(max_length=255, blank=True)
    is_ready = models.BooleanField(default=False)
    hand = models.ManyToManyField('Card')

    @classmethod
    def create(cls, username):
        player = cls(username=username)
        # do something with the book
        return player

    def __str__(self):
        return str(self.username)

    def setHand(cards):
        self.hand = cards
        self.save()

from abc import ABCMeta, abstractmethod

class Location(models.Model):
    name = models.CharField(max_length=255, blank=True)
    adjacent_locations = models.ManyToManyField('Location', through='AdjacentLocation')
    characters = models.ManyToManyField('Character')
    max_characters = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

    def get_characters(self):
        return self.characters

    def add_adjacent_location(self, location, direction):
        AdjacentLocation.create(curr_loc=self, di=direction, loc=location)

    # Locations and directions must be passed in in corresponding order
    def add_adjacent_locations(self, locations, directions):
        for idx, location in enumerate(locations):
            self.add_adjacent_location(location, directions[idx])

    # def is_valid_move_target(self):
    #     return (len(self.characters) < self.max_characters)
#
#     def get_valid_moves(self):
#         directions = []
#         for direction, location in self.adjacent_locations.iter_items():
#             if(location.is_valid_move_target()):
#                 directions.append((location, direction))
#
#     def add_character(self, character):
#         self.characters.append(character)
#
#     def remove_character(self, character):
#         self.characters.remove(character)
#
#     def is_character_in_room(self, character):
#         return character in self.characters
#
#     def north(self):
#         return self.adjacent_locations.get('N', None)
#
#     def south(self):
#         return self.adjacent_locations.get('S', None)
#
#     def east(self):
#         return self.adjacent_locations.get('E', None)
#
#     def west(self):
#         return self.adjacent_locations.get('W', None)
#
#     def secret(self):
#         return self.adjacent_locations.get('secret', None)


class Room(Location):
    @classmethod
    def create(cls, name):
      return cls(name=name, max_characters=6)

class Hallway(Location):
    @classmethod
    def create(cls, name):
      return cls(name=name, max_characters=1)

class StartRoom(Location):
    @classmethod
    def create(cls, name):
      return cls(name=name, max_characters=0)

class Character(models.Model):
    name = models.CharField(max_length=32, blank=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE, null=True)
    curr_location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True)
    selected = models.BooleanField(default=False)

    @classmethod
    def create(cls, name):
      return cls(name=name)

    # def __init__(self, name, player, location):
    #     self.name = name
    #     self.player = player
    #     self.location = location
    #
    # def __str__(self):
    #     return self.name
    #
    # def get_player(self):
    #     return self.player
    #
    # def get_location(self):
    #     return self.location
    #
    # # This function does NOT check whether the room to be moved to is a
    # # valid target, that should be checked prior to this call
    # def move_character(self, new_location):
    #     self.location.remove_character(self)
    #     new_location.add_character(self)
    #     self.location = new_location

class Card(models.Model):
    name = models.CharField(max_length=32, blank=True)
    card_type = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, card_type):
        return cls(name=name, card_type=card_type)



class Map(models.Model):
    locations = models.ManyToManyField('Location')

    @classmethod
    def create(cls):
        return cls()


    def initialize_locations(self):
        # Initialize rooms
        study = Room.create(name="Study")
        hall = Room.create(name="Hall")
        lounge = Room.create(name="Lounge")
        library = Room.create(name="Library")
        billiard_room = Room.create(name="Billiard Room")
        dining_room = Room.create(name="Dining Room")
        conservatory = Room.create(name="Conservatory")
        ballroom = Room.create(name="Ballroom")
        kitchen = Room.create(name="Kitchen")

        # Initialize hallways
        study_hall_hallway = Hallway.create("Study - Hall Hallway")
        hall_lounge_hallway = Hallway.create("Hall - Lounge Hallway")
        study_library_hallway = Hallway.create("Study - Library Hallway")
        hall_billiard_room_hallway = Hallway.create("Hall - Billiard Room Hallway")
        lounge_dining_room_hallway = Hallway.create("Lounge - Dining Room Hallway")
        library_billiard_room_hallway = Hallway.create("Library - Billiard Room Hallway")
        billiard_room_dining_room_hallway = Hallway.create("Billiard Room - Dining Room Hallway")
        library_conservatory_hallway = Hallway.create("Library - Conservatory Hallway")
        billiard_room_ballroom_hallway = Hallway.create("Billiard Room - Ballroom Hallway")
        dining_room_kitchen_hallway = Hallway.create("Dining Room - Kitchen Hallway")
        conservatory_ballroom_hallway = Hallway.create("Conservatory - Ballroom Hallway")
        ballroom_kitchen_hallway = Hallway.create("Ballroom - Kitchen Hallway")

        # Initialize start rooms
        # TODO: Add characters to these starting rooms

        scarlet_start = StartRoom.create('scarlet-start')
        plum_start = StartRoom.create('plum_start')
        mustard_start = StartRoom.create('mustard_start')
        peacock_start = StartRoom.create('peacock_start')
        green_start = StartRoom.create('green_start')
        white_start = StartRoom.create('white_start')


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


        study.save()
        hall.save()
        lounge.save()
        library.save()
        billiard_room.save()
        dining_room.save()
        conservatory.save()
        ballroom.save()
        kitchen.save()

        study_hall_hallway.save()
        hall_lounge_hallway.save()
        study_library_hallway.save()
        hall_billiard_room_hallway.save()
        lounge_dining_room_hallway.save()
        library_billiard_room_hallway.save()
        billiard_room_dining_room_hallway.save()
        library_conservatory_hallway.save()
        billiard_room_ballroom_hallway.save()
        dining_room_kitchen_hallway.save()
        conservatory_ballroom_hallway.save()
        ballroom_kitchen_hallway.save()

        scarlet_start.save()
        plum_start.save()
        mustard_start.save()
        peacock_start.save()
        green_start.save()
        white_start.save()

        self.locations.add(study)
        self.locations.add(hall)
        self.locations.add(lounge)
        self.locations.add(library)
        self.locations.add(billiard_room)
        self.locations.add(dining_room)
        self.locations.add(conservatory)
        self.locations.add(ballroom)
        self.locations.add(kitchen)

        self.locations.add(study_hall_hallway)
        self.locations.add(hall_lounge_hallway)
        self.locations.add(study_library_hallway)
        self.locations.add(hall_billiard_room_hallway)
        self.locations.add(lounge_dining_room_hallway)
        self.locations.add(library_billiard_room_hallway)
        self.locations.add(billiard_room_dining_room_hallway)
        self.locations.add(library_conservatory_hallway)
        self.locations.add(billiard_room_ballroom_hallway)
        self.locations.add(dining_room_kitchen_hallway)
        self.locations.add(conservatory_ballroom_hallway)
        self.locations.add(ballroom_kitchen_hallway)

        self.locations.add(scarlet_start)
        self.locations.add(plum_start)
        self.locations.add(mustard_start)
        self.locations.add(peacock_start)
        self.locations.add(green_start)
        self.locations.add(white_start)

        self.save()




class AdjacentLocation(models.Model):
    original_location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='orig')
    target_location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='target')
    direction = models.CharField(max_length=32, blank=True)

    @classmethod
    def create(cls, curr_loc, di, loc):
      return cls(original_location=curr_loc, direction=di, target_location=loc)
