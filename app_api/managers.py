from django.contrib.auth.models import UserManager as Manager
from django.db import models


class UserManager(Manager):
    """
    Custom user manager for handling email-based authentication.

    Methods:
        - create_user (method): Creates and saves a regular user with the given email and password.
            - Parameters:
                - email (str): The user's email address (required).
                - password (str): The user's password (optional).
                - **extra_fields: Additional fields for the user model.
            - Raises:
                - ValueError: If the email is not provided.

        - create_superuser (method): Creates and saves a superuser with elevated permissions.
            - Parameters:
                - email (str): The superuser's email address (required).
                - password (str): The superuser's password (optional).
                - **extra_fields: Additional fields for the user model.
            - Sets:
                - is_staff: True
                - is_superuser: True
            - Raises:
                - ValueError: If is_staff or is_superuser are not set to True.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        username = email.split("@")[0]
        first_name = extra_fields.pop("first_name").capitalize()
        last_name = extra_fields.pop("last_name").capitalize()
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class RoleBasedManager(UserManager):
    """Base manager for role-based proxy models."""
    role = None

    def get_queryset(self):
        if not self.role:
            raise NotImplementedError(
                "Role must be defined in the derived manager.")
        return super().get_queryset().filter(role=self.role)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    def create_user(self, email, password=None, **extra_fields):
        extra_fields["role"] = self.role
        extra_fields["username"] = self.email.split("@")[0]

        email = self.normalize_email(email)

        return super().create_user(email, password, **extra_fields)


class SuperadminManager(RoleBasedManager):
    """Custom manager for Superadmins."""

    role = "superuser"

    def get_queryset(self):
        return super().get_queryset().filter(role="superadmin")


class AdminManager(RoleBasedManager):
    """Custom manager for Admin proxy model."""

    role = "admin"

    def get_queryset(self):
        return super().get_queryset().filter(role="admin")


class TeacherManager(RoleBasedManager):
    """Custom manager for Teacher proxy model."""

    role = "teacher"

    def get_queryset(self):
        return super().get_queryset().filter(role="teacher")


class StudentManager(RoleBasedManager):
    """Custom manager for Student proxy model."""

    role = "student"

    def get_queryset(self):
        return super().get_queryset().filter(role="student")


class ParentManager(RoleBasedManager):
    """Custom manager for Parent proxy model."""

    role = "parent"

    def get_queryset(self):
        return super().get_queryset().filter(role="parent")
