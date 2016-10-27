from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.acceuil, name='acceuil'),

    url(r'^dictee_list/$', views.dictee_list, name='dictee_list'),
    url(r'^exo_dictee/(?P<pk>[0-9]+)/$', views.exo_dictee, name='exo_dictee'),

    url(r'^alphabet_list/$', views.alphabet_list, name='alphabet_list'),
    url(r'^exo_alphabet/(?P<level>[0-9]+)/$', views.exo_alphabet, name='exo_alphabet'),

]

