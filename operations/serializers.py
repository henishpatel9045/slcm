from rest_framework import serializers

from entities.serializers import InstituteSerializer
from . import models

class EnrollmentSerializers(serializers.ModelSerializer):
    institute = InstituteSerializer()
    class Meta:
        model = models.Enrollement
        fields = "__all__"


class TCSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.TransferCertificate
        fields = "__all__"
        