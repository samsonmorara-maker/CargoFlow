from apps.shipments.services.notifications import notify_driver_assigned
from apps.assignments.services.assignment import create_assignment_request


def assign_driver(shipment):
    """
    Start the driver assignment process.

    Instead of assigning a driver immediately,
    create an assignment request and wait for
    the driver to accept.
    """

    assignment = create_assignment_request(shipment)

    if assignment is None:
        return None

    # Shipment is now searching for a driver
    shipment.status = shipment.Status.PENDING
    shipment.save(update_fields=["status"])

    # Notify the driver that a new delivery request is waiting
    notify_driver_assigned(shipment)

    return assignment