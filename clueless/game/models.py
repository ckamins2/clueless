# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Game(models.Model):
    players = models.ManyToManyField('Player')
    game_map = models.ManyToManyField('Map')
    finalSolution = models.ManyToManyField('Card')

    @classmethod
    def create(cls):
        game = cls()
        # do something with the book
        return game

    def __str__(self):
        return str(self.id)

class Player(models.Model):
    username = models.CharField(max_length=255, blank=True)

    @classmethod
    def create(cls, username):
        player = cls(username=username)
        # do something with the book
        return player

    def __str__(self):
        return str(self.username)

from abc import ABCMeta, abstractmethod

class Location(models.Model):
    name = models.CharField(max_length=255, blank=True)
    adjacent_locations = models.ManyToManyField('Location')
    characters = models.ManyToManyField('Character')
    max_characters = models.IntegerField(default = 0)
#
#     def get_characters(self):
#         return self.characters
#
#     def add_adjacent_location(self, location, direction):
#         self.adjacent_locations[direction] = location
#
#     # Locations and directions must be passed in in corresponding order
#     def add_adjacent_locations(self, locations, directions):
#         for idx, location in enumerate(locations):
#             self.add_adjacent_location(location, directions[idx])
#
#     def is_valid_move_target(self):
#         return (len(self.characters) < self.max_characters)
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
    def create(cls, name, adj_loc, chars):
      return cls(name=name, adj_locations=adj_loc, characters=chars, max_characters=6)

class Hallway(Location):
    @classmethod
    def create(cls, name, adj_loc, chars):
      return cls(name=name, adj_locations=adj_loc, characters=chars, max_characters=1)

class StartRoom(Location):
    @classmethod
    def create(cls, name, adj_loc, chars):
      return cls(name=name, adj_locations=adj_loc, characters=chars, max_characters=0)

class Character(models.Model):
    name = models.CharField(max_length=32, blank=True)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    curr_location = models.ForeignKey('Location', on_delete=models.CASCADE)

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
    pass

class Map(models.Model):
    locations = models.ManyToManyField('Location')
