from datetime import timedelta

from django.utils import timezone

from apps.accounts.models import DriverProfile
from apps.assignments.models import DriverAssignmentRequest


def create_assignment_request(shipment):
    """
    Find the first available driver and create
    an assignment request.
    """

    driver_profile = (
        DriverProfile.objects.filter(
            verification_status=DriverProfile.VerificationStatus.APPROVED,
            availability_status=DriverProfile.AvailabilityStatus.ONLINE,
        )
        .select_related("user")
        .first()
    )

    if driver_profile is None:
        return None

    assignment = DriverAssignmentRequest.objects.create(
        shipment=shipment,
        driver=driver_profile.user,
        expires_at=timezone.now() + timedelta(seconds=90),
        estimated_earnings=shipment.estimated_price,
    )

    return assignment