from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .serializers import TeacherSerializer, SubjectSerializer, GroupSerializer, UserSerializer
from .models import Subject, Group, Teacher

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        role = request.GET.get("role")

        if role:
            self.queryset = self.queryset.filter(role=role)
        data = self.serializer_class(self.queryset, many=True).data

        return Response(data=data)


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "email"]


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "teacher__first_name",
                     "teacher__last_name", "subject__name"]
