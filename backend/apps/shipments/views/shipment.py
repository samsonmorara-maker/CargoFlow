from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.shipments.services.driver_assignment import assign_driver
from apps.shipments.models import Shipment
from apps.shipments.serializers import ShipmentSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "uuid"

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Shipment.objects.all()

        return Shipment.objects.filter(customer=user)

    def perform_create(self, serializer):
        shipment = serializer.save(customer=self.request.user)

        assign_driver(shipment)