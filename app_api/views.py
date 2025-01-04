from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Group, Student, Subject, Teacher
from .serializers import (
    GroupSerializer,
    StudentSerializer,
    SubjectSerializer,
    TeacherSerializer,
    UserSerializer,
)

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


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
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
    search_fields = [
        "name",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
    ]
