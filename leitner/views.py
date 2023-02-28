import json
import os
import random
from doit.blocks import *
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.serializers import UserSerializerData
from leitner.models import Pharma, Prop, Card, Daroo, FlashCard
from leitner.serializers import *
from trivia_backend.settings import PROJECT_ROOT


@api_view(['POST'])
def add_pharma(request):
    print(str(request.data).encode('utf-8'))
    pharma = Pharma.objects.create(
        group=request.data['group'],
        name=request.data['drug'],
    )

    for key, value in request.data['props'].items():
        Prop.objects.create(
            pharma=pharma,
            key=key,
            value=value
        )
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_random_pharma(request):
    if request.data['level'] == 0:

        user_cards = User.objects.get(id=request.user.id).card_set.all()
        user_pharma_id_list = map(lambda x: x.pharma.id, user_cards)
        pharma_list = list(Pharma.objects.all().exclude(id__in=user_pharma_id_list))
        random.shuffle(pharma_list)
        return Response(PharmaSerializer(pharma_list[0]).data)
    else:
        level_cards = list(Card.objects.filter(user=request.user).filter(level=request.data['level']))
        # user_pharma_id_list = map(lambda x: x.pharma.id, user_cards)
        # pharma_list = list(Pharma.objects.all().exclude(id__in=user_pharma_id_list))
        random.shuffle(level_cards)
        return Response(PharmaSerializer(level_cards[0].pharma).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cards(request):
    pharma = Pharma.objects.get(id=request.data['pharma_id'])
    card = Card()
    if request.data['is_remembered']:
        card.level = 2
    else:
        card.level = 1
    card.pharma = pharma
    card.user = request.user
    card.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_levels(request):
    levels = Card.objects.filter(user=request.user).values_list('level')
    levels = list(set(map(lambda x: x[0], list(levels))))
    print(levels)
    levels_list = []
    for i in levels:
        levels_list.append({
            'level': i,
            'cards': CardSerializer(Card.objects.filter(user=request.user).filter(level=i), many=True).data
        })

    return Response(levels_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_level_cards(request, level):
    cards = Card.objects.filter(level=level)
    return Response(CardSerializer(cards, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_card(request):
    card, created = Card.objects.get_or_create(user=request.user, pharma_id=request.data['pharma_id'])
    if request.data['is_remembered']:
        card.level = card.level + 1
        card.save()
    else:
        pass
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leader_board(request):
    users_by_leitner_points = sorted(User.objects.all(), key=lambda x: x.leitner_points, reverse=True)
    return Response(UserLitnerPointSerializer(users_by_leitner_points, many=True).data, status=status.HTTP_200_OK)


# darooooooooooooooooooo
@api_view(['POST'])
def add_daroo(request):
    print(str(request.data.dict()).encode('utf-8'))
    daroo_form = DarooSerializerInsert(data=request.data)
    # daroo = Daroo.objects.create()
    # for key, value in request.data.items():
    #     #print(str(json.dumps(json.loads(value))).encode('utf-8'))
    #     print(type(value))
    #     print(value.encode('utf-8'))
    #     #daroo[key] = json.loads(value)
    #     #daroo.save()
    if daroo_form.is_valid():
        daroo_form.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        print(daroo_form.errors)
        return Response(json.dumps(daroo_form.errors), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_random_daroo(request):
    if request.data['level'] == 0:

        user_cards = User.objects.get(id=request.user.id).flashcard_set.all()
        user_pharma_id_list = map(lambda x: x.daroo.id, user_cards)
        pharma_list = list(Daroo.objects.all().exclude(id__in=user_pharma_id_list).filter(
            block_combined__contains=request.user.block_priority))
        random.shuffle(pharma_list)
        return Response(DarooSerializer(pharma_list[0]).data)
    else:
        level_cards = list(FlashCard.objects.filter(user=request.user).filter(level=request.data['level']))
        # user_pharma_id_list = map(lambda x: x.pharma.id, user_cards)
        # pharma_list = list(Pharma.objects.all().exclude(id__in=user_pharma_id_list))
        random.shuffle(level_cards)
        return Response(DarooSerializer(level_cards[0].daroo).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cards_daroo(request):
    pharma = Daroo.objects.get(id=request.data['pharma_id'])
    card = FlashCard()
    if request.data['is_remembered']:
        card.level = 2
    else:
        card.level = 1
    card.daroo = pharma
    card.user = request.user
    card.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_levels_daroo(request):
    levels = FlashCard.objects.filter(user=request.user).values_list('level')
    levels = list(set(map(lambda x: x[0], list(levels))))
    print(levels)
    levels_list = []
    for i in levels:
        levels_list.append({
            'level': i,
            'cards': FlashCardSerializer(FlashCard.objects.filter(user=request.user).filter(level=i), many=True).data
        })

    return Response(levels_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_level_cards_daroo(request, level):
    cards = FlashCard.objects.filter(level=level)
    return Response(FlashCardSerializer(cards, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_card_daroo(request):
    card, created = FlashCard.objects.get_or_create(user=request.user, daroo_id=request.data['pharma_id'])
    if request.data['is_remembered']:
        card.level = card.level + 1
        card.save()
    else:
        pass
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leader_board_daroo(request):
    users_by_leitner_points = sorted(User.objects.all(), key=lambda x: x.leitner_points, reverse=True)
    return Response(UserLitnerPointSerializer(users_by_leitner_points, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def assign_drug(request, block):
    daroos = Daroo.objects.all()

    # with open(os.path.join(PROJECT_ROOT, f'doit/block_{block}.txt'),'r') as f:
    daroos_in_b1 = globals()[f'block_{block}']

    trues = 0
    for i in daroos_in_b1:
        for d in daroos:
            if d.name.lower() in (i.lower()) or (i.lower() in d.name.lower()):
                trues += 1
                up_d = Daroo.objects.get(id=d.id)
                up_d.block_combined = f'{up_d.block_combined},{block}'
                up_d.save()

    return Response({'trues': trues}, status=status.HTTP_418_IM_A_TEAPOT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_user_block(request):
    user = User.objects.get(id=request.user.id)
    user.block_priority = request.data['block_priority']
    user.save()
    refresh = RefreshToken.for_user(user)
    return Response({**{
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }, **dict(UserSerializerData(user).data)}, status=status.HTTP_200_OK)
