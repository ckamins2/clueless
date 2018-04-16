# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login, logout

from game.models import Player, Game, Map

class HomePageView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        characters = Game.get_current_game().get_characters()
        return render(request, 'index.html', {'ready': False, 'available_characters': characters})

@login_required
def process_ready_click(request):
    print "Processing ready";
    game = Game.get_current_game()
    players = game.get_current_game_players()
    player = game.get_current_player(request.user.username)
    if player is not None:
        player.is_ready = True
        player.save()

        print players.values_list('is_ready', flat=True)

    if(all(players.values_list('is_ready', flat=True))):
        print "Start game"
        game_map = Map.create()
        game_map.save()
        game_map.initialize_locations()
        print game_map.locations.all()
        game.game_map = game_map
        game.save()
        game.initialize_game()

        return render(request, 'game_page.html', {'ready': True})




    # TODO: Display how many players are logged in/ready/not ready
    # This is definitely NOT a priority though

    return render(request, 'ready_button.html', {'ready': True})

@login_required
def process_unready_click(request):
    print "Processing unready";
    player = Game.get_current_game().get_current_player(request.user.username)
    characters = Game.get_current_game().get_characters()
    if player is not None:
        player.is_ready = False
        player.save()

    return render(request, 'ready_button.html', {'ready': False})

@login_required

def check_available_characters(request):
    characters = Game.get_current_game().get_characters()
    player = Game.get_current_game().get_current_player(request.user.username)

    return render(request, 'available_characters.html', {'available_characters': characters})
