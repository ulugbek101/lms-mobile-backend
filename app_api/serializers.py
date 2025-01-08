from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

from .models import Subject, Group

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["full_name"] = f"{user.first_name} {user.last_name}"
        token["email"] = user.email
        token["profile_photo"] = user.profile_photo.url
        token["role"] = user.role

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PasswordHashMixin:
    def create(self, validated_data):
        # Default to None if not provided
        password = validated_data.pop("password", None)

        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializer(ModelSerializer, PasswordHashMixin):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }


class TeacherSerializer(ModelSerializer, PasswordHashMixin):
    class Meta:
        model = User
        exclude = ["last_login", "date_joined", "groups",
                   "user_permissions", "student_groups"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }


class StudentSerializer(ModelSerializer, PasswordHashMixin):
    class Meta:
        model = User
        exclude = ["last_login", "date_joined", "groups", "user_permissions"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }


class SubjectSerializer(ModelSerializer):
    students = SerializerMethodField()
    groups = SerializerMethodField()

    class Meta:
        model = Subject
        fields = "__all__"

    def get_students(self, obj):
        """
        Returns the count of unique students associated with the subject.
        """
        return User.objects.filter(student_groups__in=obj.group_set.all()).distinct().count()

    def get_groups(self, obj):
        """
        Returns the counf of unique group associated with the subject
        """
        return Group.objects.filter(subject=obj).count()


class GroupSerializer(ModelSerializer):
    teacher = TeacherSerializer()
    subject = SerializerMethodField()
    students = SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_subject(self, obj):
        return obj.subject.name

    def get_students(self, obj):
        return obj.user_set.filter(role="student").count()
