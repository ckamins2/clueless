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

        return render(request, 'index.html', context=None)
