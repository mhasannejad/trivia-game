from rest_framework.serializers import ModelSerializer

from authentication.models import User
from leitner.models import Pharma, Prop, Card


class PropSerializer(ModelSerializer):
    class Meta:
        model = Prop
        fields = ['id', 'key', 'value']


class PharmaSerializer(ModelSerializer):
    props = PropSerializer(many=True)

    class Meta:
        model = Pharma
        fields = ['id', 'group', 'name', 'props']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CardSerializer(ModelSerializer):
    user = UserSerializer()
    pharma = PharmaSerializer()

    class Meta:
        model = Card
        fields = ['id', 'level', 'user', 'pharma']
