from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet

router = DefaultRouter()
router.register("api/school", SchoolViewSet, basename="SchoolView endpoint")

urlpatterns = [
    path("", include(router.urls)),
]

