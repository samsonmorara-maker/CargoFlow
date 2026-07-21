from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.shipments.serializers import DashboardSerializer
from apps.shipments.services.dashboard import (
    get_dashboard_statistics,
)


class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = get_dashboard_statistics()

        serializer = DashboardSerializer(data)

        return Response(serializer.data)