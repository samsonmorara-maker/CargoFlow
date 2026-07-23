from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import (
    SignupView,
    LoginView,
    VehicleViewSet,
)

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicle")

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls