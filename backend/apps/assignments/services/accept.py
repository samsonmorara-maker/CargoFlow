from django.db import transaction
from django.utils import timezone

from apps.assignments.models import DriverAssignmentRequest
from apps.accounts.models import DriverProfile

from apps.shipments.models import ShipmentEvent
from apps.shipments.services.events import create_shipment_event
from apps.shipments.services.notifications import notify_driver_assigned


@transaction.atomic
def accept_assignment(assignment, driver):

    if assignment.driver != driver:
        raise ValueError("This assignment does not belong to this driver.")

    if assignment.status != DriverAssignmentRequest.Status.PENDING:
        raise ValueError("Assignment is no longer pending.")

    assignment.status = DriverAssignmentRequest.Status.ACCEPTED
    assignment.responded_at = timezone.now()
    assignment.save()

    shipment = assignment.shipment

    shipment.driver = driver
    shipment.status = shipment.Status.DRIVER_ASSIGNED
    shipment.save()

    profile = DriverProfile.objects.get(user=driver)

    profile.availability_status = (
        DriverProfile.AvailabilityStatus.BUSY
    )

    profile.save()

    create_shipment_event(
        shipment=shipment,
        event_type=ShipmentEvent.EventType.DRIVER_ASSIGNED,
        description=f"{driver.first_name} accepted the shipment.",
        performed_by=driver,
    )

    notify_driver_assigned(shipment)

    return shipment