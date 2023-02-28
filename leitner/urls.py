from django.urls import path

from .views import *

urlpatterns = [
    path('pharma/add/', add_pharma, name='add_pharma'),
    path('daroo/add/', add_daroo, name='add_daroo'),
    path('pharma/random/', get_random_pharma, name='get_random_pharma'),
    path('daroo/random/', get_random_daroo, name='get_random_daroo'),
    path('daroo/create/', add_to_cards_daroo, name='add_to_cards_daroo'),
    path('card/upgrade/', upgrade_card, name='upgrade_card'),
    path('flashcard/upgrade/', upgrade_card_daroo, name='upgrade_card_daroo'),
    path('assign/<int:block>/', assign_drug, name='assign'),
    path('card/mine/', get_my_levels, name='get_my_levels'),
    path('flashcard/mine/', get_my_levels_daroo, name='get_my_levels_daroo'),
    path('leaderboard/', leader_board, name='leader_board'),
    path('card/level/<int:level>/', get_level_cards, name='get_level_cards'),
    path('block/set/priority/', set_user_block, name='set_user_block'),
    path('flashcard/level/<int:level>/', get_level_cards_daroo, name='get_level_cards_daroo'),
]
