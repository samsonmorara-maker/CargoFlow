from rest_framework.exceptions import ValidationError
from apps.shipments.models import Shipment


def process_pickup(driver, pickup_qr_token):
    shipment = Shipment.objects.filter(
        pickup_qr_token=pickup_qr_token
    ).first()

    if not shipment:
        raise ValidationError("Invalid pickup QR code.")

    if shipment.pickup_qr_used:
        raise ValidationError("This pickup QR code has already been used.")

    if shipment.driver != driver:
        raise ValidationError(
            "You are not assigned to this shipment."
        )

    shipment.status = Shipment.Status.PICKED_UP
    shipment.pickup_qr_used = True
    shipment.save()

    return {
        "message": "Pickup confirmed successfully.",
        "delivery_address": shipment.delivery_address,
        "receiver_name": (
            f"{shipment.customer.first_name} "
            f"{shipment.customer.last_name}"
        ),
        "receiver_phone": shipment.customer.phone_number,
        "estimated_price": shipment.estimated_price,
    }