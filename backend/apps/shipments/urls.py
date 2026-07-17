from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.shipments.views import ShipmentViewSet

router = DefaultRouter()
router.register("", ShipmentViewSet, basename="shipments")

urlpatterns = [
    path("", include(router.urls)),
]