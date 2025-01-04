from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(prefix="users", viewset=views.UserViewSet, basename="users")
router.register(prefix="teachers", viewset=views.TeacherViewSet, basename="teachers")
router.register(prefix="students", viewset=views.StudentViewSet, basename="students")
router.register(prefix="subjects", viewset=views.SubjectViewSet, basename="subjects")
router.register(prefix="groups", viewset=views.GroupViewSet, basename="groups")

urlpatterns = router.urls
