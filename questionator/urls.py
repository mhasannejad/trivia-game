from django.urls import path

from .views import *

urlpatterns = [
    path('random/', get_random_question, name='rand_question'),
    path('mistake/submit/', save_mistakes, name='save_mistakes'),
    path('mistake/report/', get_my_reports, name='get_my_reports'),
    path('mistake/notes/', get_twenty_notes, name='get_twenty_notes'),

]
