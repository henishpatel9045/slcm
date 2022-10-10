import random
from sre_parse import State
from wsgiref import validate
from rest_framework import status, views, mixins, viewsets, permissions
from rest_framework.response import Response
from .models import CentralEducationDepartment, DistrictEducationDepartment, ResetOTP, StateEducationDepartment, Student, InstituteAdmin
from .serializers import CentralEducationDepartmentSerializer, DistrictEduSerializer, InstituteAdminSerializer, StateEduSerializer, StudentSerializer
import logging
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import password_changed, validate_password
from django.contrib.auth.hashers import check_password

logging.getLogger(__name__)


# Create your views here.
class StudentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        page_size = int(self.request.GET.get("page_size", 20))
        page_size = int(self.request.GET.get("page_number", 1))
        
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def get_queryset(self):
        qs = self.queryset
        user = self.request.user
        if hasattr(user, 'app_user'):
            qs = Student.objects.filter(user=user)
        elif hasattr(user, 'institute_admin'):
            qs = Student.objects.filter(enrollement__is_active=True, 
                                        enrollment__institute=user.institute_admin.institute)
        elif hasattr(user, 'central_edu'):
            qs = Student.objects.all()
        elif hasattr(user, 'state_edu'):
            qs = Student.objects.filter(state=user.state_edu.state)
        elif hasattr(user, 'district_edu'):
            qs = Student.objects.filter(state=user.district_edu.state,
                                        district=user.district_edu.district)
        
        
        logging.info(self.request.user, self.request.user.is_staff)
        return qs
    

class UserDetails(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        subject = "Endpoint Hit."
        msg = "Yep bro."
        
        send_mail(subject=subject, message=msg, recipient_list=['ompatel9045@gmail.com'], from_email="slcm.api@edu.com")
        
        user = self.request.user    
        
        if hasattr(user, 'app_user'):
            serializer = StudentSerializer
            qs = Student.objects.get(user=user)
        elif hasattr(user, 'institute_admin'):
            serializer = InstituteAdminSerializer
            qs = InstituteAdmin.objects.get(user=user)
        elif hasattr(user, 'central_edu'):
            serializer = CentralEducationDepartmentSerializer
            qs = CentralEducationDepartment.objects.get(user=user)
        elif hasattr(user, 'state_edu'):
            serializer = StateEduSerializer
            qs = StateEducationDepartment.objects.get(user=user)
        elif hasattr(user, 'district_edu'):
            serializer = DistrictEduSerializer
            qs = DistrictEducationDepartment.objects.get(user=user)
        
        if serializer:
            data = serializer(qs)   
            return Response(data.data, status=200)
        else:
            return Response({"detail": "User is not valid.", "success": False}, status=status.HTTP_400_BAD_REQUEST) 
        
        
class GenerateResetOTP(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = self.request.user
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
        
        
    