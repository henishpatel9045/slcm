import random
from sre_parse import State
from wsgiref import validate
from rest_framework import status, views, mixins, viewsets, permissions
from rest_framework.response import Response
from custom_users.resources import StudentResources

from django.shortcuts import HttpResponse

from slcm.common_serializers import PaginatorSerializer
from .models import CentralEducationDepartment, DistrictEducationDepartment, ResetOTP, StateEducationDepartment, Student, InstituteAdmin
from .serializers import CentralEducationDepartmentSerializer, DistrictEduSerializer, InstituteAdminSerializer, StateEduSerializer, StudentSerializer
import logging
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from operations.models import Enrollement

from django.contrib.auth import get_user_model, logout
from django.utils import timezone
from django.db import transaction

from django.contrib.auth.password_validation import password_changed, validate_password
from django.contrib.auth.hashers import check_password

logging.getLogger(__name__)


# Create your views here.
class StudentDetailViewSet(PaginatorSerializer):
    serializer_class = StudentSerializer
    queryset = Student.objects.select_related("user").all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if hasattr(user, 'app_user'):
            qs = Student.objects.filter(user=user)
        elif hasattr(user, 'institute_admin'):
            qs = Student.objects.filter(enrollement__is_active=True, 
                                        enrollement__institute=user.institute_admin.institute)
        elif hasattr(user, 'central_edu'):
            qs = Student.objects.all()
        elif hasattr(user, 'state_edu'):
            qs = Student.objects.filter(state=user.state_edu.state)
        elif hasattr(user, 'district_edu'):
            qs = Student.objects.filter(state=user.district_edu.state,
                                        district=user.district_edu.district)
        
        logging.info(self.request.user, self.request.user.is_staff)
        return qs
    
    # def list(self, request):
    #     page_size = int(self.request.GET.get("page_size", 20))
    #     page_number = int(self.request.GET.get("page_number", 1))
        
    #     if page_size < 1:
    #         page_size = 1
        
    #     if page_number < 1:
    #         page_number = 1
        
    #     start = (page_number-1) * page_size
    #     end = page_size * page_number
    #     total_entries = self.get_queryset().count()
    #     queryset = self.filter_queryset(self.get_queryset()[start:end])
        
    #     return_entries = queryset.count()
        
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response({"data": serializer.data, "total_entries": total_entries, "return_entries": return_entries})
    
    
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            user = self.request.user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student = serializer.save()
            headers = self.get_success_headers(serializer.data)
            
            enrollment = Enrollement()
            enrollment.student = student
            enrollment.institute = user.institute_admin.institute
            enrollment.current_year = 1
            enrollment.date_of_admission = timezone.now().date()
            enrollment.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        

class UserDetails(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        subject = "Endpoint Hit."
        msg = "Yep bro."
        
        send_mail(subject=subject, message=msg, recipient_list=['ompatel9045@gmail.com'], from_email="slcm.api@edu.com")
        
        user = self.request.user    
        
        if hasattr(user, 'app_user'):
            serializer = StudentSerializer
            qs = Student.objects.select_related("user").get(user=user)
        elif hasattr(user, 'institute_admin'):
            serializer = InstituteAdminSerializer
            qs = InstituteAdmin.objects.select_related("institute").select_related("user").get(user=user)
        elif hasattr(user, 'central_edu'):
            serializer = CentralEducationDepartmentSerializer
            qs = CentralEducationDepartment.objects.select_related("user").get(user=user)
        elif hasattr(user, 'state_edu'):
            serializer = StateEduSerializer
            qs = StateEducationDepartment.objects.select_related("user").get(user=user)
        elif hasattr(user, 'district_edu'):
            serializer = DistrictEduSerializer
            qs = DistrictEducationDepartment.objects.select_related("user").get(user=user)
        
        if serializer:
            data = serializer(qs)   
            return Response(data.data, status=200)
        else:
            return Response({"detail": "User is not valid.", "success": False}, status=status.HTTP_400_BAD_REQUEST) 
        
        
class GenerateResetOTP(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = get_user_model().objects.get(username=request.data.get("username"))
        try:
            ResetOTP.objects.create(user=user, otp=random.randint(1111, 9999))
        except Exception as e:
            return Response({"detail": "Error occurred.", "error": str(e.args[0])}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": True}, status=status.HTTP_200_OK)        
        
class PasswordReset(views.APIView):
    def post(self, request):
        User = get_user_model()
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        
        # reset = PasswordResetForm(request.POST)
        
        # if reset.is_valid():
        #     data = reset.cleaned_data['email']
        user = User.objects.get(username=username)
        
        # try:
        if check_password(password, user.password):
            return Response({"error": ["Can't use current password as new password."], "sucess": False}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password=password, user=user)
        except Exception as e:
            return Response({"error": e.args[0][0], 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        # except Exception as e:
        user.set_password(password)
        user.save()
        return Response({"detail": f"PAssword changed for user {user.username}. New password is {password}", "success": True}, status=status.HTTP_200_OK)
        
        

class Logout(views.APIView):
    def post(self, request):
        try:
            logout(request)
        except Exception as e:
            return Response({"error": str(e.args[0]), 'status': False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": True}, status=status.HTTP_200_OK)
    
    
# class DashboardView(views.APIView):
    
class ExportStudent(views.APIView):
    def get(self, request):
        print(request.user)
        user = request.user
        print(user)
        qs = Student.objects.filter(enrollement__institute=user.institute_admin.institute, enrollement__is_active=True)
        person_resource = StudentResources()
        dataset = person_resource.export()
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Students.xlsx"'
        return response 

    