from rest_framework import viewsets, permissions
from deposit.models import Deposit
from .serializers import DepositSerializer


class DepositPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
        return False
            


class DepositViewSet(viewsets.ModelViewSet):
    serializer_class = DepositSerializer
    permission_classes = [DepositPermission,]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Deposit.objects.all()
        return Deposit.objects.filter(customer=self.request.user)