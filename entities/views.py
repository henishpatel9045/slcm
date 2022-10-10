from rest_framework import viewsets, views, status

from custom_users.models import Student
from .models import Institute, School, College
from .serializers import SchoolSerializer

# # Create your views here.

# class 
class InstituteViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
   

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    