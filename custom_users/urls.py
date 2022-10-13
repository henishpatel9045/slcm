from django.urls import path, include
from rest_framework.routers import DefaultRouter

from custom_users.models import StudentChangeRequest
from .views import BulkApproveStudentEnrollement, ExportStudent, Logout, StudentDetailViewSet, StudentForApproval, StudentUpdateViewSet, UserDetails, PasswordReset
from rest_registration.api.views import send_reset_password_link

router = DefaultRouter()
router.register('student', StudentDetailViewSet, basename='student')
# For student he will get only his data, institute admin will get all the student in institute data.
router.register("student/update", StudentUpdateViewSet, basename="Update student information")
router.register("new-admission", StudentForApproval, basename="New students list for approval from higher edu department.")

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/logout', Logout.as_view()),
    path('api/reset', PasswordReset.as_view()),
    path('api/me', UserDetails.as_view()),
    path('api/student/export', ExportStudent.as_view()),
    path("api/new-admissions/approve", BulkApproveStudentEnrollement.as_view()),
    path("api/new-admissions/approve/", BulkApproveStudentEnrollement.as_view()),
]
