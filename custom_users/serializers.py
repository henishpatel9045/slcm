from rest_framework import serializers
from django.db import transaction

from entities.models import Institute
from .models import Student, InstituteAdmin, CentralEducationDepartment, StateEducationDepartment, DistrictEducationDepartment, StudentChangeRequest
from entities.serializers import InstituteSerializer
class UserSerializer(serializers.Serializer):
    pass
    

class StudentSerializer(UserSerializer, serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "Student".upper()
    
    class Meta:
        model = Student
        fields = '__all__'

class InstituteAdminSerializer(UserSerializer, serializers.ModelSerializer):
    institute = serializers.SerializerMethodField()
    def get_institute(self, obj):
        return InstituteSerializer(obj.institute).data
    
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "InstituteAdmin".upper()
    
    class Meta:
        model = InstituteAdmin
        fields = ['id', 'user_type', 'active', 'institute']

class CentralEducationDepartmentSerializer(UserSerializer, serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "CentralEduDept".upper()
    
    class Meta:
        model = CentralEducationDepartment
        fields = '__all__'

class StateEduSerializer(UserSerializer, serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "StateEduDept".upper()
    
    class Meta:
        model = StateEducationDepartment
        fields = '__all__'
        
class DistrictEduSerializer(UserSerializer, serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "DistrictEduDept".upper()
    
    class Meta:
        model = DistrictEducationDepartment
        fields = '__all__'
        

class StudentUpdateRequest(serializers.ModelSerializer):
    class Meta:
        model = StudentChangeRequest
        fields = "__all__"

    def update(self, instance, validated_data):
        if not instance.is_approved and validated_data.get("is_approved", False):
            with transaction.atomic():
                student = Student.objects.get(pk=instance.student.pk)
                for key in validated_data.keys:
                    current = getattr(student, key)
                    latest = validated_data[key]

                    if current != latest:
                        setattr(student, key, latest)
                instance.is_approved = True
                student.save()
                instance.save()
        return instance
        