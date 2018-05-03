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

from game.models import Player, Game, Map, Suggestion, Accusation, Card
from game.forms.create_game_form import CharacterForm
from game import *

class HomePageView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        all_games = Game.objects.all()
        player = Player.objects.filter(username=request.user.username).get()
        is_owner = len(all_games.filter(game_owner=player)) > 0
        in_game = len(all_games.filter(players__in=[player])) > 0
        game_pk = None

        if is_owner:
            game_pk = all_games.filter(game_owner=player).order_by('-id')[:1].get().id
        else:
            game_pk = player.get_current_game().id if player.get_current_game() != None else 0
        return render(request, 'index.html', {'in_game': in_game, 'is_owner': is_owner, 'game_pk': game_pk, 'player_count': len(player.get_current_game().players.all()) if player.get_current_game() != None else False})

@login_required
def create_game(request):
    create_game_form = CharacterForm()
    return render(request, 'create_game.html', {'create_game_form': create_game_form})

@login_required
def gen_new_game(request):
    if request.method == 'POST':
        data = request.POST
        player = Player.objects.filter(username=request.user.username).get()
        game = Game.create(player)
        character = game.characters.filter(name=data.get('character_name'))

        character = character.get()
        character.player = player;
        character.save()

        game.players.add(player)
        game.save()

    return redirect('game:home')

@login_required
def start_game(request, game_pk):
    player = Player.objects.filter(username=request.user.username).get()
    game = Game.objects.get(pk=game_pk)

    if(game.game_owner == player and game.game_state == 1):
        game.initialize_game()

    player_hand = player.get_hand()

    return render(request, "game.html", {'player_name': player.username, 'player_character': player.get_character(), 'player_hand': player_hand})

@login_required
def join_game(request):
    game_list = Game.objects.filter(game_state=1)

    games = []

    for game in game_list:
        games.append({'id': game.id, 'player_count': len(game.players.all())})

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

    return redirect('game:home')

def get_available_characters(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    characters = game.characters.filter(player=None)
    return render(request, "available_characters.html", {'game': game, 'characters': characters})


@login_required
def update_home_page(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()
    data_to_send = {'game_state': player.check_current_game_state(), 'game_id': game.id if game != None else 0, 'player_count': len(player.get_current_game().players.all()) if player.get_current_game() != None else False}
    data = json.dumps(data_to_send)
    return HttpResponse(data, content_type='application/json')

@login_required
def update_player_options(request):
    player = Player.objects.filter(username=request.user.username).get()

    game = player.get_current_game()

    if player.check_current_game_state() == GAME_STATE_FINISHED:
        if game.winner == None:
            data_to_send = {'game_state': player.check_current_game_state(), 'game_id': game.id if game != None else 0,
                        'winner': None}
        else:
            data_to_send = {'game_state': player.check_current_game_state(), 'game_id': game.id if game != None else 0,
                        'winner': game.winner.username}
        data = json.dumps(data_to_send)
        game.players.remove(player)
        player.reset()
        return HttpResponse(data, content_type='application/json')

    if(player.is_active):
        if player.turn_state == SELECTING_ACTION:
            options = []
            # Possible options:
            # 1) Player can move to room and make guess
            # 2) Player can move to hallways
            # 3) Player can stay in current room and make guess (ONLY if moved by suggestion)
            # 4) Player cannot do any of the above and must pass

            if player.can_move and len(player.get_valid_moves()) > 0 and not player.is_eliminated() and player.can_suggest:
                options.append({'id': GET_VALID_MOVES, 'text': 'Move character'})

            if player.can_make_suggestion() and not player.is_eliminated():
                options.append({'id': SELECT_SUGGESTION_CARDS, 'text': 'Make suggestion'})

            # Player can always make accusation (on their turn)
            if not player.is_eliminated():
                options.append({'id': SELECT_ACCUSATION_CARDS, 'text': 'Make accusation'})

            if player.is_eliminated() or len(player.get_valid_moves()) == 0 or (not player.can_make_suggestion() and not player.can_move):
                options.append({'id': 'pass-turn', 'text': 'Pass turn'})

            # Set up message to send back
            message = False

            if not player.can_suggest and game.active_suggestion is None:
                message = "No one refuted your suggestion!"
            if not player.can_suggest and game.active_suggestion is not None:
                message = "Your suggestion was refuted with " + game.active_suggestion.refuting_card.name + " by " + game.active_suggestion.refuting_player.username + "."

            return render(request, "action_options.html", {"messages" : [message] if message else [], "valid_options": options, "eliminated": player.is_eliminated()})
        elif player.turn_state == WAITING_ON_SUGGESTION:
            return render(request, "action_options.html", {"messages": [game.active_suggestion.player.username + " made a suggestion of " + game.active_suggestion.suspect.name + " in the " + game.active_suggestion.crime_scene.name + " with a " + game.active_suggestion.weapon.name + ".", "Waiting on " + game.get_active_player().username + " for a response."]})
        elif player.turn_state == REFUTING_SUGGESTION:
            suggestion = game.active_suggestion
            cards_to_refute = [card for card in player.get_hand() if card in [suggestion.get_suspect(), suggestion.get_weapon(), suggestion.get_crime_scene()]]
            cards_list = []
            for card in cards_to_refute:
                cards_list.append({'name': card.name.replace(' ', '-').lower(), 'text': card.name})

            message = False
            if len(cards_list) == 0:
                message = "You have no cards to refute this suggestion."
            else:
                message = "Select a valid card to refute this suggestion."

            return render(request, "refute_suggestion.html", {"messages": [game.active_suggestion.player.username + " made a suggestion of " + game.active_suggestion.suspect.name + " in the " + game.active_suggestion.crime_scene.name + " with a " + game.active_suggestion.weapon.name + ".", message], 'cards_to_refute': cards_list})
        else:
            return HttpResponse({}, content_type='application/json')
    elif player.turn_state == WAITING_ON_SUGGESTION:
        return render(request, "action_options.html", {"messages": ["You made a suggestion of " + game.active_suggestion.suspect.name + " in the " + game.active_suggestion.crime_scene.name + " with a " + game.active_suggestion.weapon.name + ".", "Waiting on " + game.get_active_player().username + " for a response."]})
    else:
        message = False
        if not game.get_active_player().can_suggest and game.active_suggestion is None:
            message = game.get_active_player().username + " did not have their suggestion refuted."
        if not game.get_active_player().can_suggest and game.active_suggestion is not None:
            message = game.active_suggestion.player.username + " had their suggestion refuted by " + game.active_suggestion.refuting_player.username + "."
        if game.active_suggestion is not None and game.get_active_player().turn_state == WAITING_ON_SUGGESTION:
            message = game.active_suggestion.player.username + " made a suggestion of " + game.active_suggestion.suspect.name + " in the " + game.active_suggestion.crime_scene.name + " with a " + game.active_suggestion.weapon.name + "."
            return render(request, "action_options.html", {"messages": [message, "Waiting on " + game.get_active_player().username + " for a response."] if message else [], "eliminated": player.is_eliminated()})
        else:
            message = game.get_active_player().username + " is taking their turn."
        return render(request, "action_options.html", {"messages": [message] if message else [], "eliminated": player.is_eliminated()})

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
    player.set_turn_state(MOVING_CHARACTER)

    return render(request, 'move_room_options.html', {"valid_rooms": valid_rooms})


@login_required
def back_to_options(request):
    player = Player.objects.filter(username=request.user.username).get()
    player.set_turn_state(SELECTING_ACTION)

    return HttpResponse({}, content_type='application/json')

@login_required
def move_to_room(request):
    if request.method == 'GET':
        data = request.GET

        player = Player.objects.filter(username=request.user.username).get()

        location = player.get_current_game().get_map().get_location(data['location'])

        player.move_to_room(location)
        player.set_player_moved()
        player.set_turn_state(SELECTING_ACTION)

    return redirect('game:update_player_options')

@login_required
def select_suggestion_cards(request):
    player = Player.objects.filter(username=request.user.username).get()
    hand = player.get_hand()

    cards = player.get_current_game().get_cards()

    location = player.get_character().get_location()

    suspect_list = []
    weapon_list = []

    for card in cards:
        card_attrs = {}
        if card in hand:
            card_attrs['in_hand'] = True
        else:
            card_attrs['in_hand'] = False

        card_attrs['name'] = card.name.replace(' ', '-').lower()
        card_attrs['type'] = card.card_type
        card_attrs['text'] = card.name

        if card.card_type == 'suspect':
            suspect_list.append(card_attrs)
        elif card.card_type == 'weapon':
            weapon_list.append(card_attrs)

    try:
        hand.get(name=location.name)
        loc_in_hand = True
    except Card.DoesNotExist:
        loc_in_hand = False


    loc_attrs = {'name': location.name.replace(' ', '-').lower(), 'in_hand': loc_in_hand, 'text': location.name}

    player.set_turn_state(MAKING_SUGGESTION)

    return render(request, 'select_suggestion_cards.html', {'suspect_list': suspect_list,
        'weapon_list': weapon_list, 'location': loc_attrs})

@login_required
def make_suggestion(request):
    if request.method == 'POST':
        data = request.POST

        player = Player.objects.filter(username=request.user.username).get()
        game = player.get_current_game()
        suggestion = Suggestion.create(player, data['suspect_options'], data['weapon_options'], data['room_options'])

        character = game.get_characters().get(name=data['suspect_options'].replace('-', ' ').title())
        location = game.get_location(data['room_options'])

        character.move_to_room(location)

        if character.get_player() != None:
            character.get_player().set_moved_by_suggestion()

        game.set_active_suggestion(suggestion)
        player.set_turn_state(WAITING_ON_SUGGESTION)
        player.has_guessed()

        game.pass_suggestion(player)

        return redirect('game:start_game', game_pk=player.get_current_game().id)

@login_required
def pass_suggestion(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        game.pass_suggestion(player)
        return redirect('game:start_game', game_pk=player.get_current_game().id)

@login_required
def refute_suggestion(request):

    if request.method == 'POST':
        data = request.POST

        player = Player.objects.filter(username=request.user.username).get()
        game = player.get_current_game()
        suggestion = game.active_suggestion

        if suggestion.get_suspect().name == data['refute_option'].replace('-', ' ').title():
            suggestion.set_refuting_card(suggestion.get_suspect())
        if suggestion.get_weapon().name == data['refute_option'].replace('-', ' ').title():
            suggestion.set_refuting_card(suggestion.get_weapon())
        if suggestion.get_crime_scene().name == data['refute_option'].replace('-', ' ').title():
            suggestion.set_refuting_card(suggestion.get_crime_scene())

        suggestion.set_refuting_player(player)
        #suggestion.set_refuting_card(suggestion.)

        player.set_turn_state(SELECTING_ACTION)
        player.make_not_active_player()

        suggestion.player.set_turn_state(SELECTING_ACTION)
        suggestion.player.make_active_player()


    return redirect('game:start_game', game_pk=player.get_current_game().id)


@login_required
def select_accusation_cards(request):
    player = Player.objects.filter(username=request.user.username).get()
    cards = player.get_current_game().get_cards()

    suspect_list = []
    weapon_list = []
    room_list = []

    for card in cards:
        if card.card_type == 'suspect':
            suspect_list.append({'name': card.name.replace(' ', '-').lower(), 'type': card.card_type, 'text': card.name})
        elif card.card_type == 'weapon':
            weapon_list.append({'name': card.name.replace(' ', '-').lower(), 'type': card.card_type, 'text': card.name})
        if card.card_type == 'room':
            room_list.append({'name': card.name.replace(' ', '-').lower(), 'type': card.card_type, 'text': card.name})

    player.set_turn_state(MAKING_ACCUSATION)

    return render(request, 'select_accusation_cards.html', {'suspect_list': suspect_list,
        'weapon_list': weapon_list, 'room_list': room_list})

@login_required
def make_accusation(request):
    if request.method == 'POST':
        data = request.POST

        player = Player.objects.filter(username=request.user.username).get()
        game = player.get_current_game()
        accusation = Accusation.create(player, data['suspect_options'], data['weapon_options'], data['room_options'])

        correct = game.check_accusation(accusation)

        if correct:
            game.winner = player
            game.set_game_state(GAME_STATE_FINISHED)
        else:
            player.set_eliminated()
            if game.is_all_eliminated():
                game.set_game_state(GAME_STATE_FINISHED)

        player.set_turn_state(SELECTING_ACTION)

        return redirect('game:start_game', game_pk=player.get_current_game().id)

@login_required
def update_map(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()

    characters = game.get_characters()

    all_data = []

    character_locs = {}

    for character in characters:
        if not character.get_location().name.replace(' ', '-').lower() in character_locs:
            character_locs[character.get_location().name.replace(' ', '-').lower()] = [character.name.replace(' ', '-').lower()]
        else:
            character_locs[character.get_location().name.replace(' ', '-').lower()].append(character.name.replace(' ', '-').lower())

    all_data.append(render(request, "game_board.html").content)
    all_data.append(character_locs)

    data = json.dumps(all_data)

    return HttpResponse(data, content_type='application/json')

def update_notebook(request):
    player = Player.objects.filter(username=request.user.username).get()
    game = player.get_current_game()
    if request.method == 'POST':
        data = request.POST
        print data

    return redirect('game:start_game', game_pk=player.get_current_game().id)
