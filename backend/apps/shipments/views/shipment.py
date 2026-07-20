from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.shipments.services.driver_assignment import assign_driver
from apps.shipments.models import Shipment
from apps.shipments.serializers import ShipmentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.shipments.serializers import PickupSerializer
from apps.shipments.services.pickup import process_pickup
from apps.shipments.serializers import DeliverySerializer
from apps.shipments.services.delivery import process_delivery
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

    @action(detail=False, methods=["post"], url_path="pickup")
    def pickup(self, request):
        serializer = PickupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = process_pickup(
            driver=request.user,
            pickup_qr_token=serializer.validated_data["pickup_qr_token"],
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=["post"], url_path="confirm-delivery")
    def confirm_delivery(self, request):
        serializer = DeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = process_delivery(
            driver=request.user,
            delivery_qr_token=serializer.validated_data.get(
            "delivery_qr_token"
            ),
            delivery_code=serializer.validated_data.get(
            "delivery_code"
            ),
        )

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="my-deliveries")
    def my_deliveries(self, request):
        """
        Return shipments assigned to the logged-in driver.
        """

        shipments = Shipment.objects.filter(driver=request.user)

        serializer = self.get_serializer(shipments, many=True)

        return Response(serializer.data)