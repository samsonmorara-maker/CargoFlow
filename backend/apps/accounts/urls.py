from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import (
    SignupView,
    LoginView,
    VehicleViewSet,
    ProfileView,
    ChangePasswordView,
    CustomerListView,
    DriverListView,
)

router = DefaultRouter()
router.register("vehicles", VehicleViewSet, basename="vehicle")

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/",ProfileView.as_view(),name="profile",),
    path("change-password/",ChangePasswordView.as_view(),name="change-password",),
    path("customers/",CustomerListView.as_view(),name="customers",),
    path("drivers/",DriverListView.as_view(),name="drivers",),
]


urlpatterns += router.urls