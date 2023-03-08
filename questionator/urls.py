from django.urls import path

from .views import *

urlpatterns = [
    path('random/', get_random_question, name='rand_question'),
    path('mistake/submit/', save_mistakes, name='save_mistakes'),

]
