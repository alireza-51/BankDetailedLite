from rest_framework import viewsets, permissions
from .serializers import UserSerializer, get_user_model

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return User.objects.all()
            else:
                return User.objects.filter(national_no=self.request.user.national_no)
        else:
            return User.objects.none()
