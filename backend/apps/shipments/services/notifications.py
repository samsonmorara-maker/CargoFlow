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