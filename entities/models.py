from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver 
from django.db.models.signals import post_save

from custom_users.model_choices import SCHOOL_BOARDS, STATES

# Create your models here.

class Institute(models.Model):
    institute_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    township = models.CharField(max_length=100, help_text="Taluka/Tehsil")
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=5, choices=STATES)
    established_year = models.IntegerField(validators=[MaxValueValidator(2022, 
                                                                        "Can't add institutes which are not currently established.")])
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return f"{self.name} - {self.city}"
    
@receiver(post_save, sender=Institute)
def create_institute_id(sender, instance, created, **kwargs):
    instance.institute_id = f"{instance.state}{(8-len(str(instance.pk)))*'0'}{instance.pk}"
    Institute.objects.filter(pk=instance.pk).update(institute_id=instance.institute_id)
    
    
class School(models.Model):
    institute = models.OneToOneField(Institute, on_delete=models.CASCADE, related_name='school')
    lowest_standard = models.IntegerField(default=1, 
                                          validators=[MinValueValidator(1, "Can't have standard lower than 1."), 
                                                      MaxValueValidator(12, "Can't have standard higher than 12.")])
    highest_standard = models.IntegerField(default=12, 
                                          validators=[MinValueValidator(1, "Can't have standard lower than 1."), 
                                                      MaxValueValidator(12, "Can't have standard higher than 12.")])
    
    board = models.CharField(max_length = 50,choices = SCHOOL_BOARDS, default ="State")
    
    
    def __str__(self):
        return f"{self.institute.name} - {self.institute.city}"
    
    
class College(models.Model):
    institute = models.OneToOneField(Institute, on_delete=models.CASCADE, related_name='college')
    
    def __str__(self):
        return f"{self.institute.name} - {self.institute.city}"
