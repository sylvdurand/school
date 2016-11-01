from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.acceuil, name='acceuil'),

    url(r'^dictee_list/$', views.dictee_list, name='dictee_list'),
    url(r'^exo_dictee/(?P<pk>[0-9]+)/$', views.exo_dictee, name='exo_dictee'),
    url(r'^dictee_new/$', views.dictee_new, name='dictee_new'),



    url(r'^alphabet_list/$', views.alphabet_list, name='alphabet_list'),
    url(r'^exo_alphabet/(?P<level>[0-9]+)/$', views.exo_alphabet, name='exo_alphabet'),
    url(r'^exo_ecrire_alphabet/(?P<level>[0-9]+)/$', views.exo_ecrire_alphabet, name='exo_ecrire_alphabet'),

    url(r'^math_acceuil/(?P<type>[a-z]+)/$', views.math_acceuil, name='math_acceuil'),
    url(r'^math_calcul/(?P<type>[a-z]+)/(?P<chiffre>[1-9]+)$', views.math_calcul, name='math_calcul'),
    url(r'^exo_probleme/(?P<pk>[1-9]+)$', views.exo_probleme, name='exo_probleme'),

]

