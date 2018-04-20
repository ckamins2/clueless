"""clueless URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

from game.models import Game, Player

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^', include('game.urls', namespace='game')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()

# Comment this out if you need to wipe database
#game = Game.create()
#game.initialize_game()


def player_login(sender, user, request, **kwargs):
    print "Logged in!"
    print request.user.username
    player = Player.create(request.user.username)
    player.save()

def player_logout(sender, user, request, **kwargs):
    print "Logged out!"
    print request.user.username
    try:
        player = Player.objects.all().filter(username=request.user.username)
        player.delete()
    except Player.DoesNotExist:
        print 'This got weird'

user_logged_in.connect(player_login)
user_logged_out.connect(player_logout)
