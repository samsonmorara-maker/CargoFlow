from apps.shipments.models import ShipmentEvent


def create_shipment_event(
    shipment,
    event_type,
    description,
    performed_by=None,
):
    ShipmentEvent.objects.create(
        shipment=shipment,
        event_type=event_type,
        description=description,
        performed_by=performed_by,
    )