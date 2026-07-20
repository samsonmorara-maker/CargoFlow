from apps.accounts.models import DriverProfile
from apps.shipments.services.notifications import notify_driver_assigned
from apps.shipments.services.events import create_shipment_event
from apps.shipments.models import ShipmentEvent


def assign_driver(shipment):
    """
    Automatically assign the best available driver.
    """
    driver_profile = (
        DriverProfile.objects.filter(
            verification_status=DriverProfile.VerificationStatus.APPROVED,
            availability_status=DriverProfile.AvailabilityStatus.ONLINE,
        )
        .order_by(
            "completed_deliveries",
            "-rating",
        )
        .first()
    )
    if not driver_profile:
        return None

    shipment.driver = driver_profile.user
    shipment.status = shipment.Status.DRIVER_ASSIGNED
    shipment.save()

    driver_profile.availability_status = (
        DriverProfile.AvailabilityStatus.BUSY
    )
    driver_profile.save()
    notify_driver_assigned(shipment)

    # Record the event
    create_shipment_event(
        shipment=shipment,
        event_type=ShipmentEvent.EventType.DRIVER_ASSIGNED,
        description=(
            f"Driver {driver_profile.user.first_name} "
            f"{driver_profile.user.last_name} was assigned."
        ),
        performed_by=driver_profile.user,
    )
    return driver_profile.user