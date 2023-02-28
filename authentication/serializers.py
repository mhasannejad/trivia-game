from rest_framework.serializers import ModelSerializer, ReadOnlyField

from authentication.models import User
from core.models import Level


class UserSerializerData(ModelSerializer):
    symbol_name = ReadOnlyField()
    level = ReadOnlyField()
    is_valid_to_moderate = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'role', 'level', 'is_valid_to_moderate', 'block_priority']


class UserSerializerProfile(ModelSerializer):
    symbol_name = ReadOnlyField()
    ranking = ReadOnlyField()
    stats = ReadOnlyField()
    points = ReadOnlyField()
    level = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'ranking', 'stats', 'points', 'level']
