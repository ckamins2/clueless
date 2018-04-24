# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from random import shuffle

from game import *

# Create your models here.

class Game(models.Model):
    players = models.ManyToManyField('Player')
    game_map = models.ForeignKey('Map', null=True)
    case_file = models.ManyToManyField('Card', related_name='case_file')
    characters = models.ManyToManyField('Character')
    game_state = models.IntegerField(default=0)
    game_owner = models.ForeignKey('Player', related_name='owner')

    player_taking_turn = models.ForeignKey('Player', related_name='player_taking_turn', null=True)

    winner = models.ForeignKey('Player', related_name='winner', null=True)

    active_suggestion = models.ForeignKey('Suggestion', related_name='active_suggestion', null=True)

    @classmethod
    def create(cls, game_owner):
        game = cls()
        game.game_owner = game_owner
        game.game_state = GAME_STATE_CREATED
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
        return self.characters.all()

    def get_cards(self):
        return Card.objects.filter(game=self)

    def get_card(self, name):
        return Card.objects.get(game=self, name=name)

    def createCharacters(self):
        col_mustard = Character.create('Colonel Mustard')
        miss_scarlet = Character.create('Miss Scarlet')
        prof_plum = Character.create('Professor Plum')
        mr_green = Character.create('Mr Green')
        mrs_white = Character.create('Mrs White')
        mrs_peacock = Character.create('Mrs Peacock')

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
        game_map = Map.create()
        game_map.save()
        game_map.initialize_locations()
        self.game_map = game_map
        self.save()
        for player in self.players.all():
            player.reset()
        cards = self.initialize_cards()
        print "Cards initialized"
        print cards
        cards = self.shuffle_cards(cards)
        print "Cards shuffled"
        cards = self.get_case_file(cards)
        self.pass_out_cards(cards)
        self.game_state = GAME_STATE_STARTED

        print self.case_file.all()

        self.player_taking_turn = self.players.all().first()

        #print player_taking_turn
        self.player_taking_turn.make_active_player()
        self.player_taking_turn.set_turn_state(SELECTING_ACTION)

        self.add_characters_to_map()

        self.save()


    def initialize_cards(self):
        col_mustard = Card.create('Colonel Mustard', 'suspect', self)
        miss_scarlet = Card.create('Miss Scarlet', 'suspect', self)
        prof_plum = Card.create('Professor Plum', 'suspect', self)
        mr_green = Card.create('Mr Green', 'suspect', self)
        mrs_white = Card.create('Mrs White', 'suspect', self)
        mrs_peacock = Card.create('Mrs Peacock', 'suspect', self)

        rope = Card.create('Rope', 'weapon', self)
        lead_pipe = Card.create('Lead Pipe', 'weapon', self)
        knife = Card.create('Knife', 'weapon', self)
        wrench = Card.create('Wrench', 'weapon', self)
        candlestick = Card.create('Candlestick', 'weapon', self)
        revolver = Card.create('Revolver', 'weapon', self)

        study = Card.create("Study", 'room', self)
        hall = Card.create("Hall", 'room', self)
        lounge = Card.create("Lounge", 'room', self)
        library = Card.create("Library", 'room', self)
        billiard_room = Card.create("Billiard Room", 'room', self)
        dining_room = Card.create("Dining Room", 'room', self)
        conservatory = Card.create("Conservatory", 'room', self)
        ballroom = Card.create("Ballroom", 'room', self)
        kitchen = Card.create("Kitchen", 'room', self)

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
        shuffle(cards)
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

    def get_next_player(self, curr_player):
        player_list = list(self.players.all())

        curr_player_idx = 0

        for x in range(0, len(player_list)):
            if(curr_player == player_list[x]):
                curr_player_idx = x

        next_player = player_list[curr_player_idx+1 if curr_player_idx != len(player_list) - 1 else 0]

        return next_player

    def pass_turn(self, curr_player):

        next_player = self.get_next_player(curr_player)

        curr_player.make_not_active_player()
        # Just set this to default action
        curr_player.reset_moved_by_suggestion()
        curr_player.reset_can_move()
        curr_player.reset_can_suggest()
        curr_player.set_turn_state(SELECTING_ACTION)

        next_player.make_active_player()
        next_player.set_turn_state(SELECTING_ACTION)
        next_player.reset_can_move()

    def get_player_character(self, player):
        character = self.characters.filter(player__in=[player]).get()
        return character

    def add_characters_to_map(self):

        locations = self.game_map.locations.all()
        characters = self.characters.all()

        scarlet_start = locations.get(name='scarlet-start')
        plum_start = locations.get(name='plum-start')
        mustard_start = locations.get(name='mustard-start')
        peacock_start = locations.get(name='peacock-start')
        green_start = locations.get(name='green-start')
        white_start = locations.get(name='white-start')

        col_mustard = characters.get(name='Colonel Mustard')
        miss_scarlet = characters.get(name='Miss Scarlet')
        prof_plum = characters.get(name='Professor Plum')
        mr_green = characters.get(name='Mr Green')
        mrs_white = characters.get(name='Mrs White')
        mrs_peacock = characters.get(name='Mrs Peacock')

        col_mustard.curr_location = mustard_start
        mustard_start.characters.add(col_mustard)
        col_mustard.save()
        mustard_start.save()

        miss_scarlet.curr_location = scarlet_start
        scarlet_start.characters.add(miss_scarlet)
        miss_scarlet.save()
        scarlet_start.save()

        prof_plum.curr_location = plum_start
        plum_start.characters.add(prof_plum)
        prof_plum.save()
        plum_start.save()

        mr_green.curr_location = green_start
        green_start.characters.add(mr_green)
        mr_green.save()
        green_start.save()

        mrs_white.curr_location = white_start
        white_start.characters.add(mrs_white)
        mrs_white.save()
        white_start.save()

        mrs_peacock.curr_location = peacock_start
        peacock_start.characters.add(mrs_peacock)
        mrs_peacock.save()
        peacock_start.save()

    def get_map(self):
        return self.game_map

    def check_accusation(self, accusation):
        print self.case_file.all()
        if (accusation.get_suspect() in self.case_file.all() and
            accusation.get_weapon() in self.case_file.all() and
            accusation.get_crime_scene() in self.case_file.all()):
            return True
        else:
            return False

    def set_game_state(self, state):
        self.game_state = state
        self.save()

    def is_all_eliminated(self):
        for player in self.players.all():
            if not player.is_eliminated():
                return False

        return True

    def get_active_player(self):
        for player in self.players.all():
            if player.is_active:
                return player
        return None

    def set_active_suggestion(self, suggestion):
        self.active_suggestion = suggestion
        self.save()

    def reset_active_suggestion(self):
        self.active_suggestion = None
        self.save()

    def pass_suggestion(self, curr_active_player):

        print "***** PASSING SUGGESTION *****"
        next_player = self.get_next_player(curr_active_player)

        curr_active_player.make_not_active_player()

        print str(curr_active_player != self.active_suggestion.player)
        if(curr_active_player != self.active_suggestion.player):
            curr_active_player.set_turn_state(SELECTING_ACTION)

        print "Next player: " + str(next_player)

        print "Player after next player: " + str(self.get_next_player(next_player))

        print "Is next player suggestor: "  + str(next_player == self.active_suggestion.player)

        next_player.make_active_player()

        print self.active_suggestion

        if next_player == self.active_suggestion.player:
            print "Made it all the away around"
            self.reset_active_suggestion()
            next_player.set_turn_state(SELECTING_ACTION)
            return

        next_player.set_turn_state(REFUTING_SUGGESTION)

    def get_location(self, name):
        return self.game_map.get_location(name)


class Player(models.Model):
    username = models.CharField(max_length=255, blank=True)
    is_ready = models.BooleanField(default=False)
    hand = models.ManyToManyField('Card')
    is_active = models.BooleanField(default=False)
    turn_state = models.IntegerField(default=1)
    can_move = models.BooleanField(default=True)
    can_suggest = models.BooleanField(default=True)
    eliminated = models.BooleanField(default=False)
    moved_by_suggestion = models.BooleanField(default=False)

    @classmethod
    def create(cls, username):
        player = cls(username=username)
        # do something with the book
        return player

    def __str__(self):
        return str(self.username)

    def setHand(self, cards):
        self.hand = cards
        self.save()

    def get_hand(self):
        return self.hand.all()

    def get_character(self):
        try:
            game = Game.objects.filter(players__in=[self]).get()
            return game.get_characters().get(player=self)
        except Game.DoesNotExist:
            return 0

    def check_current_game_state(self):
        try:
            game = Game.objects.filter(players__in=[self]).get()
            return game.game_state
        except Game.DoesNotExist:
            return 0

    def get_current_game(self):
        try:
            return Game.objects.filter(players__in=[self]).get()
        except Game.DoesNotExist:
            return None

    def make_active_player(self):
        self.is_active = True
        self.save()

    def make_not_active_player(self):
        self.is_active = False
        self.save()

    def set_turn_state(self, state):
        self.turn_state = state
        self.save()

    def set_player_moved(self):
        self.can_move = False
        self.save()

    def reset_can_move(self):
        self.can_move = True
        self.save()

    def set_eliminated(self):
        self.eliminated = True
        self.save()

    def set_moved_by_suggestion(self):
        self.moved_by_suggestion = True
        self.save()

    def reset_moved_by_suggestion(self):
        self.moved_by_suggestion = False
        self.save()

    def is_eliminated(self):
        return self.eliminated

    def can_player_move(self):
        return self.can_move

    def get_valid_moves(self):
        character = self.get_current_game().get_player_character(self)
        return character.get_valid_moves()

    def move_to_room(self, target_location):
        character = self.get_current_game().get_player_character(self)
        print character
        character.move_to_room(target_location)

    def reset_can_suggest(self):
        self.can_suggest = True
        self.save()

    def has_guessed(self):
        self.can_suggest = False
        self.save()

    def reset(self):
        for card in self.hand.all():
            self.hand.remove(card)
        self.is_ready = False
        self.turn_state = SELECTING_ACTION
        self.can_move = True
        self.can_suggest = True
        self.eliminated = False
        self.is_active = False
        self.moved_by_suggestion = False
        self.save()

    def can_make_suggestion(self):
        return ((not self.can_move and self.get_character().get_location().is_room()) or self.moved_by_suggestion) and self.can_suggest

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
        adj_loc = AdjacentLocation.create(curr_loc=self, di=direction, loc=location)
        adj_loc.save()

    # Locations and directions must be passed in in corresponding order
    def add_adjacent_locations(self, locations, directions):
        for idx, location in enumerate(locations):
            self.add_adjacent_location(location, directions[idx])

    def is_valid_move_target(self):
        return self.max_characters > len(self.characters.all())

    def get_valid_moves(self):
        adj_loc_list = list(self.adjacent_locations.all())

        valid_moves = []

        for location in adj_loc_list:
            if location.is_valid_move_target():
                valid_moves.append(location.name.replace(' ', '-').lower())
        return valid_moves

    def remove_character(self, character):
        self.characters.remove(character)
        self.save()

    def add_character(self, character):
        self.characters.add(character)
        self.save()

    def is_room(self):
        return self.name in ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']

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

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        return cls(name=name)

    def get_location(self):
        return self.curr_location

    def get_valid_moves(self):
        return self.curr_location.get_valid_moves()

    def move_to_room(self, target_location):
        print self.curr_location
        print target_location
        self.curr_location.remove_character(self)
        target_location.add_character(self)
        self.curr_location = target_location
        self.save()

        print self.curr_location

    def get_player(self):
        return self.player


class Card(models.Model):
    name = models.CharField(max_length=32, blank=True)
    card_type = models.CharField(max_length=32, blank=True)
    game = models.ForeignKey('Game', related_name='card_game')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, card_type, game):
        return cls(name=name, card_type=card_type, game=game)



class Map(models.Model):
    locations = models.ManyToManyField('Location')

    @classmethod
    def create(cls):
        return cls()

    def get_location(self, name):
        print name

        return self.locations.get(name=name.replace('-', ' ').title())


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
        study_hall_hallway = Hallway.create("Study To Hall Hallway")
        hall_lounge_hallway = Hallway.create("Hall To Lounge Hallway")
        study_library_hallway = Hallway.create("Study To Library Hallway")
        hall_billiard_room_hallway = Hallway.create("Hall To Billiard Room Hallway")
        lounge_dining_room_hallway = Hallway.create("Lounge To Dining Room Hallway")
        library_billiard_room_hallway = Hallway.create("Library To Billiard Room Hallway")
        billiard_room_dining_room_hallway = Hallway.create("Billiard Room To Dining Room Hallway")
        library_conservatory_hallway = Hallway.create("Library To Conservatory Hallway")
        billiard_room_ballroom_hallway = Hallway.create("Billiard Room To Ballroom Hallway")
        dining_room_kitchen_hallway = Hallway.create("Dining Room To Kitchen Hallway")
        conservatory_ballroom_hallway = Hallway.create("Conservatory To Ballroom Hallway")
        ballroom_kitchen_hallway = Hallway.create("Ballroom To Kitchen Hallway")

        # Initialize start rooms
        # TODO: Add characters to these starting rooms

        scarlet_start = StartRoom.create('scarlet-start')
        plum_start = StartRoom.create('plum-start')
        mustard_start = StartRoom.create('mustard-start')
        peacock_start = StartRoom.create('peacock-start')
        green_start = StartRoom.create('green-start')
        white_start = StartRoom.create('white-start')

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


class Guess(models.Model):
    game = models.ForeignKey('Game', related_name='accuse_game')
    player = models.ForeignKey('Player', related_name='accuse_player')
    suspect = models.ForeignKey('Card', related_name='suspect')
    weapon = models.ForeignKey('Card', related_name='weapon')
    crime_scene = models.ForeignKey('Card', related_name='crime_scene')


    def __str__(self):
        return self.suspect.name + ":" + self.weapon.name + ":" + self.crime_scene.name

    def get_suspect(self):
        return self.suspect

    def get_weapon(self):
        return self.weapon

    def get_crime_scene(self):
        return self.crime_scene


class Suggestion(Guess):
    refuting_card = models.ForeignKey('Card', related_name='evidence', null=True)
    refuting_player = models.ForeignKey('Player', related_name='refuting_player', null=True)
    @classmethod
    def create(cls, player, suspect_name, weapon_name, room_name):
      game = player.get_current_game()
      suggestion = cls(game=game, player=player, suspect=game.get_card(suspect_name.replace('-', ' ').title()),
            weapon=game.get_card(weapon_name.replace('-', ' ').title()),
            crime_scene=game.get_card(room_name.replace('-', ' ').title()))
      suggestion.save()
      return suggestion

    def set_refuting_card(self, card):
         self.refuting_card = card
         self.save()

    def set_refuting_player(self, player):
        self.refuting_player = player
        self.save()

class Accusation(Guess):
    @classmethod
    def create(cls, player, suspect_name, weapon_name, room_name):
      game = player.get_current_game()
      accusation = cls(game=game, player=player, suspect=game.get_card(suspect_name.replace('-', ' ').title()),
            weapon=game.get_card(weapon_name.replace('-', ' ').title()),
            crime_scene=game.get_card(room_name.replace('-', ' ').title()))
      accusation.save()
      return accusation
