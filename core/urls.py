from django.urls import path

from core.views import *

urlpatterns = [
    path('subjects/all/', all_subjects),
    path('users/ranking/', get_ranking),
    path('users/profile/<int:id>/', get_user_profile),
    path('challenge/available/', get_available_challenges),
    path('challenge/available/foruser/', get_available_challenges_for_user),
    path('qustion/create/', create_question),
    path('challenge/create/', create_challenge),
    path('challenge/someone/', challenge_someone),
    path('challenge/join/', join_challenge),
    path('challenge/join/invitation/', join_challenge_by_invitation),
    path('challenge/mine/', get_user_challenges),
    path('challenge/result/', get_challenge_result),
    path('challenge/result/mine/', get_user_results),
    path('challenge/submit/', submit_answer),
    path('challenge/get/<int:id>/', get_challenge_details),
]
