from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepositViewSet

router = DefaultRouter()
router.register(r'deposit', DepositViewSet, basename='deposit')

urlpatterns = router.urls