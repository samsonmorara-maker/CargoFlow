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
from apps.shipments.services.events import create_shipment_event
from apps.shipments.serializers import TrackingSerializer
from apps.shipments.serializers import CancelShipmentSerializer
from apps.shipments.services.cancel import cancel_shipment
from django.utils import timezone
from apps.shipments.serializers import DashboardSerializer
from apps.accounts.models import User
from apps.shipments.serializers import DriverDashboardSerializer
class ShipmentViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = "uuid"
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Shipment.objects.all()

        if user.role == User.Role.DRIVER:
            return Shipment.objects.filter(driver=user)

        return Shipment.objects.filter(customer=user)

    def perform_create(self, serializer):
        shipment = serializer.save(customer=self.request.user)
        create_shipment_event(
            shipment=shipment,
            event_type="CREATED",
            description="Shipment was created.",
            performed_by=self.request.user,
            )

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
    def pickup_details(self, request, uuid=None):
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
                "pickup_code": shipment.pickup_code,
                "pickup_address": shipment.pickup_address,

                "driver_name": (
                    f"{shipment.driver.first_name} {shipment.driver.last_name}"
                    if shipment.driver else None
                    ),
                "driver_phone": (
                    shipment.driver.phone_number
                    if shipment.driver else None
                ),
                "vehicle_type": (
                    shipment.driver.vehicle.vehicle_type
                    if shipment.driver and hasattr(shipment.driver, "vehicle")
                    else None
                ),
                "vehicle_number_plate": (
                    shipment.driver.vehicle.number_plate
                    if shipment.driver and hasattr(shipment.driver, "vehicle")
                    else None
                ),
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
    
    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, uuid=None):
        shipment = self.get_object()

        if (
            shipment.customer != request.user
            and not request.user.is_staff
        ):
            return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CancelShipmentSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        cancel_shipment(
            shipment=shipment,
            user=request.user,
            reason=serializer.validated_data["reason"],
        )

        return Response(
            {
            "message": "Shipment cancelled successfully."
            },
            status=status.HTTP_200_OK,
            )

    @action(detail=False,methods=["get"],url_path=r"track/(?P<tracking_number>[^/.]+)",)
    def track(self, request, tracking_number=None):
        shipment = Shipment.objects.filter(
            tracking_number=tracking_number
        ).first()

        if shipment is None:
            return Response(
                {"detail": "Shipment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            shipment.customer != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TrackingSerializer(shipment)

        return Response(serializer.data)
    @action(detail=False, methods=["get"], url_path="my-deliveries")
    def my_deliveries(self, request):
        """
        Return shipments assigned to the logged-in driver.
        """

        shipments = Shipment.objects.filter(driver=request.user)

        serializer = self.get_serializer(shipments, many=True)

        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="driver-dashboard")
    def driver_dashboard(self, request):
        if request.user.role != "DRIVER":
            return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.now().date()

        assigned = Shipment.objects.filter(driver=request.user)

        data = {
        "active_deliveries": assigned.filter(
            status=Shipment.Status.IN_TRANSIT
        ).count(),

        "pending_pickups": assigned.filter(
            status=Shipment.Status.DRIVER_ASSIGNED
        ).count(),

        "completed_today": assigned.filter(
            status=Shipment.Status.DELIVERED,
            delivery_confirmed_at__date=today,
        ).count(),

        "total_completed": assigned.filter(
            status=Shipment.Status.DELIVERED,
        ).count(),

        "in_transit": assigned.filter(
            status=Shipment.Status.IN_TRANSIT,
        ).count(),
        }

        serializer = DriverDashboardSerializer(data)

        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path="history")
    def history(self, request):
        """
     Return completed deliveries for the logged-in driver.
        """

        shipments = Shipment.objects.filter(
            driver=request.user,
            status=Shipment.Status.DELIVERED,
        ).order_by("-updated_at")

        serializer = self.get_serializer(
        shipments,
        many=True,
        )

        return Response(serializer.data)