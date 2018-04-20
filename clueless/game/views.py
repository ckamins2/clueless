# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login, logout

from game.models import Player, Game, Map
from game.forms.create_game_form import CharacterForm
from game import *

class HomePageView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        all_games = Game.objects.all()
        player = Player.objects.filter(username=request.user.username)
        is_owner = len(all_games.filter(game_owner=player)) > 0
        in_game = len(all_games.filter(players__in=player)) > 0
        game_pk = None
        print is_owner
        print in_game

        if is_owner:
            game_pk = all_games.filter(game_owner=player).get().id
        else:
            game_pk = player.get().get_current_game().id if player.get().get_current_game() != None else 0
        return render(request, 'index.html', {'in_game': in_game, 'is_owner': is_owner, 'game_pk': game_pk})

@login_required
def create_game(request):
    create_game_form = CharacterForm()
    return render(request, 'create_game.html', {'create_game_form': create_game_form})

@login_required
def gen_new_game(request):
    if request.method == 'POST':
        data = request.POST
        print data.get('character_id')
        player = Player.objects.filter(username=request.user.username).get()
        game = Game.create(player)
        character = game.characters.filter(name=data.get('character_name'))

        character = character.get()
        character.player = player;
        character.save()

        game.players.add(player)
        game.save()
        print character

    return redirect('game:home')

@login_required
def start_game(request, game_pk):
    player = Player.objects.filter(username=request.user.username).get()
    game = Game.objects.get(pk=game_pk)
    if(game.game_owner == player and game.game_state == 1):
        game.initialize_game()

    player_hand = player.get_hand()

    return render(request, "game.html", {'player_id': player.id, 'player_hand': player_hand})

@login_required
def join_game(request):
    games = Game.objects.filter(game_state=1)
    print games

    return render(request, "join_game.html", {'games': games})

@login_required
def join_target_game(request, game_pk):

    if request.method == 'POST':
        data = request.POST

        game = Game.objects.get(pk=game_pk)
        player = Player.objects.filter(username=request.user.username).get()
        character = game.characters.get(name=data.get('character'))

        character.player = player
        character.save()

        game.players.add(player)

        game.save()

        print character

    return redirect('game:home')

def get_available_characters(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    characters = game.characters.filter(player=None)
    return render(request, "available_characters.html", {'game': game, 'characters': characters})


@login_required
def update_home_page(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()
    data_to_send = {'game_state': player.check_current_game_state(), 'game_id': game.id if game != None else 0}
    data = json.dumps(data_to_send)
    return HttpResponse(data, content_type='application/json')

@login_required
def update_player_options(request):
    player = Player.objects.filter(username=request.user.username).get()

    if(player.is_active):
        if player.turn_state == SELECTING_ACTION:
            options = []
            if player.can_move :
                options.append({'id': GET_VALID_MOVES, 'text': 'Move character'})
            options.append({'id': 'pass-turn', 'text': 'Pass turn'})
            return render(request, "action_options.html", {"valid_options": options})
        else:
            return HttpResponse({}, content_type='application/json')

    else:
        return render(request, "action_options.html", {"valid_options": []})

@login_required
def pass_turn(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()

    game.pass_turn(player)

    return HttpResponse({}, content_type='application/json')

@login_required
def get_valid_moves(request):
    player = Player.objects.filter(username=request.user.username).get()
    valid_moves = player.get_valid_moves()

    valid_rooms = []

    for move in valid_moves:
        valid_rooms.append({'id': move, 'text': move.replace('-', ' ').title()})

    valid_rooms.append({'id': 'back', 'text': 'Back'})

    print valid_moves

    player.set_turn_state(MOVING_CHARACTER)

    return render(request, 'move_room_options.html', {"valid_rooms": valid_rooms})



@login_required
def move_character(request):
    pass

@login_required
def back_to_options(request):
    player = Player.objects.filter(username=request.user.username).get()
    player.set_turn_state(SELECTING_ACTION)

    return HttpResponse({}, content_type='application/json')
