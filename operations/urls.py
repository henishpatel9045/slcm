from django.urls import path, include
from . import views

urlpatterns = [
    path("api/admin/dashboard,", views.DashboardAPI.as_view()),
    path("api/admin/dashboard/", views.DashboardAPI.as_view()),
    path("api/student/<str:pk>/institutes/", views.StudentInstituteAPI.as_view()),
    path("api/student/<str:pk>/institutes", views.StudentInstituteAPI.as_view()),
    path("api/transfer/", views.GenerateTCView.as_view()),
    path("api/tc-list/", views.GenerateTCView.as_view()),
    path("api/tc-list", views.GenerateTCView.as_view()),
    path("api/transfer/<str:tc_id>/pdf", views.SendMail.as_view()),
    path("api/transfer/create-bulk", views.GenerateBulkTCView.as_view()),
]
