from rest_framework import viewsets, permissions
from .serializers import BranchSerializer, Branch


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAdminUser,]