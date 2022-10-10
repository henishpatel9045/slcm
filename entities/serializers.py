from rest_framework import serializers

from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Institute
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer
    
    class Meta:
        model = School
        fields = "__all__"
