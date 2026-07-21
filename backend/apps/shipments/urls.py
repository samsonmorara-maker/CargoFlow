from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.shipments.views import (
    ShipmentViewSet,
    DashboardView,
)

router = DefaultRouter()
router.register("", ShipmentViewSet, basename="shipment")

urlpatterns = [
    path(
        "admin/dashboard/",
        DashboardView.as_view(),
        name="admin-dashboard",
    ),
]

urlpatterns += router.urls