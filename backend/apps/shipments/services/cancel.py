from django.utils import timezone
from rest_framework.exceptions import ValidationError
from apps.shipments.services.notifications import ( notify_shipment_cancelled,notify_customer_shipment_cancelled)
from apps.accounts.models import DriverProfile
from apps.shipments.models import Shipment, ShipmentEvent
from apps.shipments.services.events import create_shipment_event


def cancel_shipment(
    shipment,
    user,
    reason,
):
    """
    Cancel a shipment.
    """

    if shipment.status not in (
        Shipment.Status.PENDING,
        Shipment.Status.CONFIRMED,
        Shipment.Status.DRIVER_ASSIGNED,
    ):
        raise ValidationError(
            "This shipment can no longer be cancelled."
        )

    shipment.status = Shipment.Status.CANCELLED
    shipment.cancelled_at = timezone.now()
    shipment.cancellation_reason = reason
    shipment.cancelled_by = user

    shipment.save()

    if shipment.driver:
        driver_profile = DriverProfile.objects.filter(
            user=shipment.driver
        ).first()
    if driver_profile:
        driver_profile.availability_status = (
            DriverProfile.AvailabilityStatus.ONLINE
        )

        driver_profile.save()

    create_shipment_event(
        shipment=shipment,
        event_type=ShipmentEvent.EventType.CANCELLED,
        description=reason,
        performed_by=user,
    )
    notify_shipment_cancelled(shipment)
    notify_customer_shipment_cancelled(shipment)


    return shipment
