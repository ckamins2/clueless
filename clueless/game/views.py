# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login, logout

from game.models import Player, Game

class HomePageView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', {'ready': False})

@login_required
def process_ready_click(request):
    print "Processing ready";
    game = Game.get_current_game()
    players = game.get_current_game_players()
    player = game.get_current_player(request.user.username)
    if player is not None:
        player.is_ready = True
        player.save()

    if(all(players.values_list('is_ready'))):
        print "Start game"

    # TODO: Display how many players are logged in/ready/not ready
    # This is definitely NOT a priority though

    return render(request, 'index.html', {'ready': True})

@login_required
def process_unready_click(request):
    print "Processing unready";
    player = Game.get_current_game().get_current_player(request.user.username)
    if player is not None:
        player.is_ready = False
        player.save()

    return render(request, 'index.html', {'ready': False})
