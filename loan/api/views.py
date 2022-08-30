from rest_framework import viewsets, permissions
from .serializers import Loan, LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Loan.objects.all()
        else:
            return Loan.objects.filter(customer=self.request.user)