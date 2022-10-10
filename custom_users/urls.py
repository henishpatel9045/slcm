from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentDetailViewSet, UserDetails, PasswordReset
from rest_registration.api.views import send_reset_password_link

router = DefaultRouter()
router.register('student', StudentDetailViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('api/reset', PasswordReset.as_view()),
    path('api/me', UserDetails.as_view()),
]
