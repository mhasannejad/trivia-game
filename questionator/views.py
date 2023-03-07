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
    random_drugs = Daroo.objects.order_by('?').filter(block_combined__contains=request.user.block_priority)[:100]
    cates = [
        'which_is_brand_name_for',
        'which_is_dosage_form_for'
    ]
    generated = []
    for i in random_drugs:
        try:
            q_type = getattr(questionator.generator, random.choice(cates))
            generated.append(q_type(i))
        except Exception as e:
            print(e)
            continue

    #q = getattr(questionator.generator, random.choice(cates))

    return Response(generated)
