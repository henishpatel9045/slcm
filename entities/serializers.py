from rest_framework import serializers

from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Institute
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer()
    
    def create(self, validated_data):
        ["institute_id",
        "name",
        "address",
        "city",
        "pincode",
        "township",
        "district",
        "state",
        "established_year",
        "is_active"]
        
        data = {}
        for d in data:
            data[d] = validated_data.get(d)
            
        institute = InstituteSerializer(data)
        institute.is_valid(data = institute.data, raise_exception=True)
        
        institute.create()
        
        return super().create(validated_data)
    
    class Meta:
        model = School
        fields = "__all__"

class CollegeSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer()