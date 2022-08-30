from rest_framework import viewsets, permissions
from deposit.models import Deposit
from .serializers import DepositSerializer


class DepositViewSet(viewsets.ModelViewSet):
    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Deposit.objects.all()
        return Deposit.objects.filter(customer=self.request.user)