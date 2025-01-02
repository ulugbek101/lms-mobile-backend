from django.db.models import TextChoices


class Roles(TextChoices):
    ADMIN = "admin", "Admin"
    TEACHER = "teacher", "Ustoz"
    PARENT = "parent", "Ota-Ona"
    STUDENT = "student", "O'quvchi"


class LessonDays(TextChoices):
    odd = "1-3-5", "Du, Cho, Jum"
    even = "2-4-6", "Se, Pay, Sha"
