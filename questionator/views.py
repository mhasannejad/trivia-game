import json
import random

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import questionator
from leitner.models import Daroo
from questionator.generator import which_is_brand_name_for


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_random_question(request):
    # unicodeData.encode('ascii', 'ignore')
    random_drugs = Daroo.objects.order_by('?').filter(block_combined__contains=request.user.block_priority)[:100]
    cates = [
        'which_is_brand_name_for',
        'which_is_dosage_form_for',
        'which_is_daroo_for_brand_name',
        'which_is_correct_pregnancy_category_for',
        'which_is_correct_pharmacologic_category_for',
        'which_is_a_treatment_category_for_daroo',
        'which_is_a_indication_for_daroo',
        'which_is_a_mechanism_for_daroo'
    ]
    generated = []
    for i in random_drugs:
        q_type = getattr(questionator.generator, random.choice(cates))

        try:
            generated.append(q_type(i))

        except Exception as e:
            print('error' + str(e.args))
            continue

    # q = getattr(questionator.generator, random.choice(cates))
    print(len(generated))
    return Response(generated)
