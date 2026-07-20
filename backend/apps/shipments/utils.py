import random


def generate_delivery_code():
    """
    Generate a unique 6-digit delivery code.
    """
    from apps.shipments.models import Shipment

    while True:
        code = str(random.randint(100000, 999999))

        if not Shipment.objects.filter(delivery_code=code).exists():
            return code