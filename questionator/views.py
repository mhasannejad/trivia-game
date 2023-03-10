import json
import random

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import questionator
from leitner.models import Daroo
from questionator.generator import which_is_brand_name_for
from questionator.models import *


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_random_question(request):
    # unicodeData.encode('ascii', 'ignore')
    random_drugs = Daroo.objects.order_by('?').filter(block_combined__contains=request.user.block_priority)[:150]
    cates = [
        'which_is_brand_name_for',
        'which_is_dosage_form_for',
        'which_is_daroo_for_brand_name',
        'which_is_correct_pregnancy_category_for',
        'which_is_correct_pharmacologic_category_for',
        'which_is_a_treatment_category_for_daroo',
        'which_is_a_indication_for_daroo',
        'which_is_a_mechanism_for_daroo',
        'which_is_a_attention_case_for_daroo',
        'which_is_a_prescription_attention_case_for_daroo',
        'which_is_a_prescription_tracking_point_case_for_daroo'
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


@api_view(['post'])
@permission_classes([IsAuthenticated])
def save_mistakes(request):
    cat,_ = QCategory.objects.get_or_create(
        name=request.data['category']
    )
    question = Questionate.objects.create(
        title=request.data['question'],
        category_id=cat.id
    )
    answer_id = None
    for i in request.data['options']:
        option = Optionate.objects.create(
            option=i['option'],
            is_right=i['is_right']
        )
        if i['option'] == request.data['answer']:
            answer_id = option.id
        question.optionate_set.add(option)

    UserAnswer.objects.create(
        user_id=request.user.id,
        question=question,
        answer_id=answer_id,
        daroo_id=request.data['daroo_id']
    )
    return Response(status=status.HTTP_201_CREATED)
