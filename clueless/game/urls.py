from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^ready/', views.process_ready_click, name='ready'),
    url(r'^unready/', views.process_unready_click, name='unready'),
    url(r'^characters/', views.check_available_characters, name='check_available_characters'),
]
