from apps.accounts.models import DriverProfile


def assign_driver(shipment):
    """
    Finds the best available driver and assigns
    the shipment automatically.
    """

    available_driver = (
        DriverProfile.objects.filter(
            verification_status="VERIFIED",
            availability_status="AVAILABLE",
        )
        .order_by("-rating", "completed_deliveries")
        .first()
    )

    if not available_driver:
        return None

    shipment.driver = available_driver.user
    shipment.status = shipment.Status.DRIVER_ASSIGNED
    shipment.save()

    return available_driver.user