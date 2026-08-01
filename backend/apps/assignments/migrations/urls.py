from rest_framework.routers import DefaultRouter

from apps.assignments.views import AssignmentViewSet

router = DefaultRouter()

router.register("", AssignmentViewSet, basename="assignments",)

urlpatterns = router.urls