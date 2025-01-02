from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager, TeacherManager, AdminManager, ParentManager, StudentManager
from .utils import Roles


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Fields:
        - username (CharField): Optional username field retained for compatibility. Not used for authentication.
        - email (EmailField): Primary field for authentication, must be unique.
        - first_name (CharField): User's first name.
        - last_name (CharField): User's last name.
        - profile_photo (ImageField): Optional profile photo for the user. Defaults to "media/users/user-default.png".

    Meta:
        - constraints: Ensures that the combination of first_name and last_name is unique.

    Additional Attributes:
        - USERNAME_FIELD (str): Specifies 'email' as the field used for authentication.
        - REQUIRED_FIELDS (list): Specifies fields required when creating a superuser (first_name, last_name).

    Methods:
        - __str__: Returns the user's full name if available, otherwise the email.
    """

    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        default="users/user-default.png", upload_to="users/", blank=True
    )
    role = models.CharField(max_length=10,
                            choices=Roles.choices,
                            default=Roles.STUDENT)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_full_name"
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_teacher(self):
        return self.role == "teacher"

    @property
    def is_parent(self):
        return self.role == "parent"

    @property
    def is_student(self):
        return self.role == "student"

class Teacher(User):
    """
    Proxy model for teachers.

    This model represents users with the role of 'teacher'.
    """

    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Student(User):
    """
    Proxy model for students.

    This model represents users with the role of 'student'.
    """

    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Parent(User):
    """
    Proxy model for parents.

    This model represents users with the role of 'parent'.
    """

    objects = ParentManager()

    class Meta:
        proxy = True
        verbose_name = "Parent"
        verbose_name_plural = "Parents"


class Admin(User):
    """
    Proxy model for admins.

    This model represents users with the role of 'admin'.
    """

    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
