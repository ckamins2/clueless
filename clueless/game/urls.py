from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^create_game/', views.create_game, name='create_game'),
    url(r'^gen_new_game/', views.gen_new_game, name='gen_new_game'),
    url(r'^start_game/(?P<game_pk>[0-9]+)/$', views.start_game, name='start_game'),
    url(r'^join_game/', views.join_game, name='join_game'),
    url(r'^join_target_game/(?P<game_pk>[0-9]+)/$', views.join_target_game, name='join_target_game'),
    url(r'^get_available_characters/(?P<game_pk>[0-9]+)/$', views.get_available_characters, name='get_available_characters'),
]
