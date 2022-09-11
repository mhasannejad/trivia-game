# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import User


@api_view(['POST'])
def register(request):
    user = User.objects.create(email=request.data['email'])
    user.set_password(request.data['password'])
    return Response(status=status.HTTP_200_OK)
