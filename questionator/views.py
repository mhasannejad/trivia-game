import json
import random

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import questionator
from authentication.serializers import UserSerializerData
from leitner.models import Daroo
from leitner.serializers import DarooMiniSerializer
from questionator.generator import which_is_brand_name_for
from questionator.models import *

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
    'which_is_a_prescription_tracking_point_case_for_daroo',
    'which_is_a_correct_training_point_for',
    'which_is_correct_lactation_category_for'
]


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_random_question(request):
    # unicodeData.encode('ascii', 'ignore')
    random_drugs = Daroo.objects.order_by('?').filter(block_combined__contains=request.user.block_priority)
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
        'which_is_a_prescription_tracking_point_case_for_daroo',
        'which_is_a_correct_training_point_for',
        'which_is_correct_lactation_category_for'
    ]
    print('cates:: '+request.user.question_categories)
    if len(str(request.user.question_categories).strip()) > 0:
        print(request.user.question_categories)

        cates = str(request.user.question_categories).split(',')
        cates = [x for x in cates if x != '']
    generated = []
    for i in range(150):
        q_type = getattr(questionator.generator, random.choice(cates))

        try:
            generated.append(q_type(random.choice(random_drugs)))

        except Exception as e:
            print('error' + str(e.args))
            continue

    # q = getattr(questionator.generator, random.choice(cates))
    print(len(generated))
    return Response(generated)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_avalible_question_categories(request):
    return Response(cates)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def set_question_categories(request):
    user = User.objects.get(id=request.user.id)
    user.question_categories = request.data['question_categories'][0:]
    print(request.data['question_categories'][1:])
    user.save()
    refresh = RefreshToken.for_user(request.user)
    return Response({**{
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }, **dict(UserSerializerData(user).data)},status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def save_mistakes(request):
    cat, _ = QCategory.objects.get_or_create(
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


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_my_reports(request):
    report = UserAnswer.objects.filter(user_id=request.user.id).values('daroo_id').annotate(Count('daroo_id'))

    full_report = []
    for i in report:
        daroo = Daroo.objects.get(id=i['daroo_id'])
        full_report.append({
            'daroo': {
                'id': daroo.id,
                'name': json.loads(daroo.name)
            },
            'count': i['daroo_id__count']
        })
    return Response(full_report)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_twenty_notes(request):
    my_answers = UserAnswer.objects.filter(user_id=request.user.id).order_by('?')[:20]
    encoded_answers = []
    for i in my_answers:
        answer = ''
        for a in i.question.optionate_set.all():

            if a.is_right:
                answer = a.option
        encoded_answers.append({
            'question': i.question.title,
            'daroo': {
                'id': i.daroo.id,
                'name': json.loads(i.daroo.name)
            },
            'answer': answer
        })

    return Response(
        encoded_answers
    )


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_daroo_details(request):
    daroo = Daroo.objects.get(id=request.data['daroo_id'])
    return Response({
        'name': json.loads(daroo.name),
        'brand_names': json.loads(daroo.tradeNames),
        'pharmacology_category': json.loads(daroo.tradeNames),
        'treatment_category': json.loads(daroo.tradeNames),
        'pregnancy_category': json.loads(daroo.tradeNames),
        'iranian_generic_products': json.loads(daroo.tradeNames),
        'indications': json.loads(daroo.tradeNames),
        'pharmacoDynamics': json.loads(daroo.tradeNames),
        'contraindications': json.loads(daroo.tradeNames),

    })
