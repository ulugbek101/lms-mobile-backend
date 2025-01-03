from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .serializers import UserSerializer, SubjectSerializer
from .models import Subject

User = get_user_model()


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        role = request.GET.get("role")

        if role:
            self.queryset = self.queryset.filter(role=role)
        data = self.serializer_class(self.queryset, many=True).data

        return Response(data=data)


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]
