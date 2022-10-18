from django.urls import path

from drug.views import *

urlpatterns = [
    path('init/db/', init_drugs),
    path('init/db/web/', init_drugs_web),
    path('questions/one/', fill_the_dosage_question),
    path('drug/list/', get_drug_list),
    path('prescription/upload/', upload_prescription),
    path('prescription/random/', get_random_prescription_to_label),
    path('prescription/tomoderate/', get_prescription_with_items_for_moderation),
    path('prescription/submit/drug/', submit_drug_to_prescription),
    path('prescription/submit/verification/', add_verification_for_prescription),
    path('profile/mine/', prescription_profile_for_user),
    path('ranking/', ranking),
    path('drug/subset/<str:drug>/', get_subsets_for),
]
