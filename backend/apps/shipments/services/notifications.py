def notify_driver_assigned(shipment):
    """
    Notify the customer that a driver has been assigned.
    This is a placeholder implementation.
    """

    message = (
        f"Hello {shipment.customer.first_name}, "
        f"your shipment has been assigned to a driver. "
        f"The driver is on the way to pick up your package."
    )

    print("=" * 60)
    print("CUSTOMER NOTIFICATION")
    print(f"To: {shipment.customer.email}")
    print(message)
    print("=" * 60)

    return message

def notify_delivery_completed(shipment):
    """
    Notify the customer that delivery is complete.
    """

    message = (
        f"Hello {shipment.customer.first_name}, "
        f"your shipment has been delivered successfully."
    )

    print("=" * 60)
    print("DELIVERY NOTIFICATION")
    print(f"To: {shipment.customer.email}")
    print(message)
    print("=" * 60)

    return message

def notify_shipment_cancelled(shipment):
    if shipment.driver:
        print(
            f"[NOTIFICATION] Shipment "
            f"{shipment.tracking_number} "
            f"was cancelled. Driver "
            f"{shipment.driver.first_name} "
            f"{shipment.driver.last_name} "
            f"is now available."
        )

def notify_customer_shipment_cancelled(shipment):
    print(
        f"[NOTIFICATION] Dear "
        f"{shipment.customer.first_name}, "
        f"your shipment "
        f"{shipment.tracking_number} "
        f"has been cancelled."
    )