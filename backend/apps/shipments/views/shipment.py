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
from apps.shipments.serializers import PickupDetailsSerializer
from apps.shipments.serializers import DeliveryDetailsSerializer
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
        received_by_name=serializer.validated_data.get(
        "received_by_name"
        ),
        received_by_phone=serializer.validated_data.get(
        "received_by_phone"
        ),
        )

        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"], url_path="pickup-details")
    def pickup_details(self, request, pk=None):
        shipment = self.get_object()

        if (
            shipment.customer != request.user
            and not request.user.is_staff
        ):
            return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
        )

        serializer = PickupDetailsSerializer(
            {
            "tracking_number": shipment.tracking_number,
            "pickup_qr_token": shipment.pickup_qr_token,
            "pickup_address": shipment.pickup_address,
            }
        )

        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path="delivery-details")
    def delivery_details(self, request, uuid=None):
        shipment = Shipment.objects.filter(uuid=uuid).first()

        if shipment is None:
            return Response(
            {"detail": "Shipment not found."},
            status=status.HTTP_404_NOT_FOUND,
            )

        if (
            shipment.driver != request.user
            and not request.user.is_staff
        ):
            return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
            )

        serializer = DeliveryDetailsSerializer(
            {
            "tracking_number": shipment.tracking_number,
            "delivery_qr_token": shipment.delivery_qr_token,
            "delivery_code": shipment.delivery_code,
            "delivery_address": shipment.delivery_address,
            "estimated_price": shipment.estimated_price,
            }
        )

        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="my-deliveries")
    def my_deliveries(self, request):
        """
        Return shipments assigned to the logged-in driver.
        """

        shipments = Shipment.objects.filter(driver=request.user)

        serializer = self.get_serializer(shipments, many=True)

        return Response(serializer.data)
    

