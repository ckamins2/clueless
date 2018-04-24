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
    url(r'^update_home_page/', views.update_home_page, name='update_home_page'),
    url(r'^update_player_options/', views.update_player_options, name='update_player_options'),
    url(r'^turn_pass/', views.pass_turn, name='pass_turn'),
    url(r'^back/', views.back_to_options, name='back'),
    url(r'^get_valid_moves/', views.get_valid_moves, name='get_valid_moves'),
    url(r'^move_to_room/', views.move_to_room, name='move_to_room'),
    url(r'^select_suggestion_cards', views.select_suggestion_cards, name='select_suggestion_cards'),
    url(r'^make_suggestion', views.make_suggestion, name='make_suggestion'),
    url(r'^pass_suggestion', views.pass_suggestion, name='pass_suggestion'),
    url(r'^refute_suggestion', views.refute_suggestion, name='refute_suggestion'),
    url(r'^select_accusation_cards', views.select_accusation_cards, name='select_accusation_cards'),
    url(r'^make_accusation', views.make_accusation, name='make_accusation'),
    url(r'^update_map', views.update_map, name='update_map'),
]
