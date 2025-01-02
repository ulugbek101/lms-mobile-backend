from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
