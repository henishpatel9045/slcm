from rest_framework import serializers
from .models import Student, InstituteAdmin, CentralEducationDepartment, StateEducationDepartment, DistrictEducationDepartment

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
    user_type = serializers.SerializerMethodField()
    def get_user_type(self, obj):
        return "InstituteAdmin".upper()
    
    class Meta:
        model = InstituteAdmin
        fields = '__all__'

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
        