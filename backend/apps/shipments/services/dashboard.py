from apps.accounts.models import User
from apps.accounts.models import DriverProfile
from apps.shipments.models import Shipment


def get_dashboard_statistics():
    return {
        "total_shipments": Shipment.objects.count(),

        "pending_shipments": Shipment.objects.filter(
            status=Shipment.Status.PENDING
        ).count(),

        "driver_assigned": Shipment.objects.filter(
            status=Shipment.Status.DRIVER_ASSIGNED
        ).count(),

        "in_transit": Shipment.objects.filter(
            status=Shipment.Status.IN_TRANSIT
        ).count(),

        "delivered": Shipment.objects.filter(
            status=Shipment.Status.DELIVERED
        ).count(),

        "cancelled": Shipment.objects.filter(
            status=Shipment.Status.CANCELLED
        ).count(),

        "total_customers": User.objects.filter(
            role=User.Role.CUSTOMER
        ).count(),

        "total_drivers": User.objects.filter(
            role=User.Role.DRIVER
        ).count(),

        "available_drivers": DriverProfile.objects.filter(
            availability_status=DriverProfile.AvailabilityStatus.ONLINE
        ).count(),

        "busy_drivers": DriverProfile.objects.filter(
            availability_status=DriverProfile.AvailabilityStatus.BUSY
        ).count(),

        "offline_drivers": DriverProfile.objects.filter(
            availability_status=DriverProfile.AvailabilityStatus.OFFLINE
        ).count(),
    }