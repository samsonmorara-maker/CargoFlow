from django.db import transaction
from django.utils import timezone

from apps.assignments.models import DriverAssignmentRequest
from apps.accounts.models import DriverProfile

from apps.assignments.services.assignment import create_assignment_request


@transaction.atomic
def decline_assignment(assignment, driver):

    if assignment.driver != driver:
        raise ValueError("This assignment does not belong to this driver.")

    if assignment.status != DriverAssignmentRequest.Status.PENDING:
        raise ValueError("Assignment is no longer pending.")

    assignment.status = DriverAssignmentRequest.Status.DECLINED
    assignment.responded_at = timezone.now()
    assignment.save()

    profile = DriverProfile.objects.get(user=driver)

    profile.availability_status = (
        DriverProfile.AvailabilityStatus.ONLINE
    )

    profile.save()

    create_assignment_request(
        assignment.shipment
    )

    return assignment