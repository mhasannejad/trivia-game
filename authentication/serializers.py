from rest_framework.serializers import ModelSerializer, ReadOnlyField

from authentication.models import User


class UserSerializerData(ModelSerializer):
    symbol_name = ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'symbol_name', 'role']
