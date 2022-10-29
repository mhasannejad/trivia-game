from django.urls import path

from .views import *

urlpatterns = [
    path('pharma/add/', add_pharma, name='add_pharma'),
    path('pharma/random/', get_random_pharma, name='get_random_pharma'),
    path('card/create/', add_to_cards, name='add_to_cards'),
    path('card/upgrade/', upgrade_card, name='upgrade_card'),
    path('card/mine/', get_my_levels, name='get_my_levels'),
    path('card/level/<int:level>/', get_level_cards, name='get_level_cards'),
]
