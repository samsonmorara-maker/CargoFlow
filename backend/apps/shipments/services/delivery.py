from rest_framework.exceptions import ValidationError

from apps.shipments.models import Shipment
from apps.accounts.models import DriverProfile
from apps.shipments.services.notifications import notify_delivery_completed


def process_delivery(driver, delivery_qr_token=None, delivery_code=None):
    """
    Confirm delivery using either a QR token
    or the manual delivery code.
    """

    if delivery_qr_token:
        shipment = Shipment.objects.filter(
            delivery_qr_token=delivery_qr_token
        ).first()

    else:
        shipment = Shipment.objects.filter(
            delivery_code=delivery_code
        ).first()

    if not shipment:
        raise ValidationError("Invalid delivery confirmation.")

    if shipment.status != Shipment.Status.PICKED_UP:
        raise ValidationError(
            "Shipment has not been picked up."
        )

    if shipment.driver != driver:
        raise ValidationError(
            "You are not assigned to this shipment."
        )

    if shipment.delivery_code_used:
        raise ValidationError(
        "Delivery has already been confirmed."
    )

    shipment.status = Shipment.Status.DELIVERED
    shipment.delivery_qr_used = True

    # Invalidate the backup code
    shipment.delivery_code = ""

    shipment.save()

    driver_profile = DriverProfile.objects.get(
        user=driver
    )

    driver_profile.availability_status = (
        DriverProfile.AvailabilityStatus.ONLINE
    )

    driver_profile.completed_deliveries += 1

    driver_profile.save()

    notify_delivery_completed(shipment)

    return {
        "message": "Delivery confirmed successfully.",
        "tracking_number": shipment.tracking_number,
        "status": shipment.status,
    }