from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from leitner.models import Pharma, Prop, Card, Daroo


class PropSerializer(ModelSerializer):
    class Meta:
        model = Prop
        fields = ['id', 'key', 'value']


class PharmaSerializer(ModelSerializer):
    props = PropSerializer(many=True)

    class Meta:
        model = Pharma
        fields = ['id', 'group', 'name', 'props']


class DarooSerializer(ModelSerializer):
    class Meta:
        model = Daroo
        fields = ['id', 'clinicalAttentions', 'pregnancyCategory', 'tradeNames', 'contraindications', 'pregnancy',
                  'treatmentCategory', 'name', 'pharmacologyCategory', 'iranianGenericProducts', 'indications',
                  'pharmacoDynamics', 'interactions', 'sideEffects', 'breastFeeding', 'trainings','block_combined']


class DarooSerializerInsert(ModelSerializer):
    class Meta:
        model = Daroo
        fields = ['clinicalAttentions', 'pregnancyCategory', 'tradeNames', 'contraindications', 'pregnancy',
                  'treatmentCategory', 'name', 'pharmacologyCategory', 'iranianGenericProducts', 'indications',
                  'pharmacoDynamics', 'interactions', 'sideEffects', 'breastFeeding', 'trainings']

    def create(self, validated_data):
        obj = Daroo.objects.create(**validated_data)
        print(str(validated_data).encode('utf-8'))
        for i in validated_data:
            print(i)
            #print(k)
        return obj


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


class UserLitnerPointSerializer(ModelSerializer):
    leitner_points = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'leitner_points']


class FlashCardSerializer(ModelSerializer):
    user = UserSerializer()
    daroo = DarooSerializer()

    class Meta:
        model = Card
        fields = ['id', 'level', 'user', 'daroo']
