# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login, logout

from game.models import Player, Game, Map
from game.forms.create_game_form import CharacterForm

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
    print game_pk
    game = Game.objects.get(pk=game_pk)
    game.initialize_game()

    return render(request, "game.html", {})

@login_required
def join_game(request):
    games = Game.objects.filter(is_active=True)
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
