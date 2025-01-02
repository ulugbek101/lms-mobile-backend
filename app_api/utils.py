from django.db.models import TextChoices


class Roles(TextChoices):
    ADMIN = "admin", "Admin"
    TEACHER = "teacher", "Ustoz"
    PARENT = "parent", "Ota-Ona"
    STUDENT = "student", "O'quvchi"
