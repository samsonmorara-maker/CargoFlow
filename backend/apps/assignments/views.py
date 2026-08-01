from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.assignments.services.decline import decline_assignment
from apps.assignments.models import DriverAssignmentRequest
from apps.assignments.serializers import AssignmentResponseSerializer
from apps.assignments.services.accept import accept_assignment


class AssignmentViewSet(viewsets.GenericViewSet):

    queryset = DriverAssignmentRequest.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    @action(detail=True, methods=["post"])
    def accept(self, request, uuid=None):

        assignment = self.get_object()

        try:
            accept_assignment(
                assignment=assignment,
                driver=request.user,
            )

            serializer = AssignmentResponseSerializer(
                {
                    "message": "Assignment accepted successfully."
                }
            )

            return Response(serializer.data)

        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @action(detail=False, methods=["get"])
    def my_requests(self, request):

        assignments = (
        DriverAssignmentRequest.objects.filter(
            driver=request.user,
            status=DriverAssignmentRequest.Status.PENDING,
        )
        .select_related("shipment", "shipment__customer")
        .order_by("-created_at")
        )

        data = []

        for assignment in assignments:
            shipment = assignment.shipment

            data.append(
                {
                    "assignment_uuid": assignment.uuid,
                    "shipment_uuid": shipment.uuid,
                    "tracking_number": shipment.tracking_number,
                    "customer_name": f"{shipment.customer.first_name} {shipment.customer.last_name}",
                    "pickup_address": shipment.pickup_address,
                    "delivery_address": shipment.delivery_address,
                    "package_name": shipment.package_name,
                    "estimated_price": shipment.estimated_price,
                    "expires_at": assignment.expires_at,
                }
            )

        return Response(data)

    @action(detail=True, methods=["post"])
    def decline(self, request, uuid=None):
        assignment = self.get_object()

        try:

            decline_assignment(
                assignment=assignment,
                driver=request.user,
            )

            return Response(
                {
                "message": "Assignment declined."
                }
            )

        except ValueError as e:
            return Response({"detail": str(e)},status=400,)