from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "date_joined", "groups", "user_permissions"]
        kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def create(self, validated_data):
        """
        Override the create method to handle password hashing.
        """
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.password = make_password(password)
            user.username = user.email.split("@")[0]
            user.save()
        return user
