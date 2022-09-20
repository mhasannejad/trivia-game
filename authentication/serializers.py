from rest_framework.serializers import ModelSerializer, ReadOnlyField

from authentication.models import User


class UserSerializerData(ModelSerializer):
    symbol_name = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'role']


class UserSerializerProfile(ModelSerializer):
    symbol_name = ReadOnlyField()
    ranking = ReadOnlyField()
    stats = ReadOnlyField()
    points = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'ranking', 'stats', 'points']
