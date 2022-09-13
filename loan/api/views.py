from rest_framework import viewsets, permissions
from .serializers import Loan, LoanSerializer

class LoanPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
        return False

class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [LoanPermission,]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Loan.objects.all()
        else:
            return Loan.objects.filter(customer=self.request.user)