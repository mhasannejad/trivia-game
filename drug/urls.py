from django.urls import path

from drug.views import *

urlpatterns = [
    path('init/db/', init_drugs),
    path('questions/one/', fill_the_dosage_question),
    path('drug/list/', get_drug_list),
    path('drug/subset/<str:drug>/', get_subsets_for),
]
