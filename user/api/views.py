from rest_framework import viewsets, permissions, exceptions
from .serializers import UserSerializer, get_user_model

User = get_user_model()

class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if request.user == obj:
            return True
        return False


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserPermissions,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return User.objects.all()
            else:
                return User.objects.filter(national_no=self.request.user.national_no)
        else:
            raise exceptions.NotAuthenticated()
