import random

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from leitner.models import Pharma, Prop, Card
from leitner.serializers import PharmaSerializer, CardSerializer


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
