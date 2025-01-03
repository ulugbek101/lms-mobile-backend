from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager, TeacherManager, AdminManager, ParentManager, StudentManager
from .utils import Roles, LessonDays


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Fields:
        - username (CharField): Optional username field retained for compatibility. Not used for authentication.
        - email (EmailField): Primary field for authentication, must be unique.
        - first_name (CharField): User's first name.
        - last_name (CharField): User's last name.
        - profile_photo (ImageField): Optional profile photo for the user. Defaults to "media/users/user-default.png".
        - roles (CharField): User's role for the system. Defaults to "student". Choices: "admin", "teacher", "parent", "student".

    Meta:
        - constraints: Ensures that the combination of first_name and last_name is unique.

    Additional Attributes:
        - USERNAME_FIELD (str): Specifies 'email' as the field used for authentication.
        - REQUIRED_FIELDS (list): Specifies fields required when creating a superuser (first_name, last_name).

    Methods:
        - __str__: Returns the user's full name if available, otherwise the email.
    """
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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
    student_groups = models.ManyToManyField(to="Group")

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_full_name"
            )
        ]

    def save(self, *args, **kwargs):
        """
        Override the save method to handle password changes securely.
        """

        self.username = self.email.split("@")[0]

        if self.pk:
            existing_user = User.objects.get(pk=self.pk)

            if existing_user.password != self.password:
                self.set_password(self.password)
        else:
            self.set_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if self.first_name and self.last_name
            else self.email
        )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

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


class Subject(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.PROTECT)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    lesson_days = models.CharField(max_length=5, choices=LessonDays.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    lesson_start_time = models.TimeField()
    lesson_end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.full_name}"


class Lesson(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(to=Group, on_delete=models.PROTECT)
    theme = models.CharField(max_length=200)
    lesson_date = models.DateField()

    def __str__(self):
        return self.theme


class Attendance(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.PROTECT)
    student = models.ForeignKey(to=Student, on_delete=models.PROTECT)
    is_absent = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.is_absent}"
