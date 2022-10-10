from datetime import datetime
import logging
from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail


from custom_users.model_choices import ADDRESS_TYPE, CAST, CURRENT_STATUS_STUDENT, GENDER, STATES
from entities.models import Institute

# Create your models here.
class CommonInfo(models.Model):
    """
    This model is used to store common information for all the models
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='app_user', blank=True)
    id = models.CharField(max_length=12, primary_key=True, blank=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=False, null=False, default="Male")
    address_line = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    pin_code = models.CharField(max_length=6, blank=False, null=False)
    township = models.CharField(max_length=50, blank=False, null=False, help_text="Taluka/Tehsil")
    district = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=5, blank=False, null=False, choices=STATES)
    phone = models.CharField(max_length=10, blank=False, null=False, 
                             validators=[RegexValidator(regex='^[0-9]*$',
                                                        message='Number should only contains integers.')])
    father_phone = models.CharField(max_length=10, blank=False, null=False, 
                             validators=[RegexValidator(regex='^[0-9]*$',
                                                        message='Number should only contains integers.')])
    mother_phone = models.CharField(max_length=10, blank=False, null=False, 
                             validators=[RegexValidator(regex='^[0-9]*$',
                                                        message='Number should only contains integers.')])
    
    class Meta:
        abstract = True


class Student(CommonInfo):
    email = models.EmailField(null=True)
    registered_year = models.IntegerField(validators=[MinValueValidator(2012, "Can only add students registered after 2012")])    
    date_of_birth = models.DateField()
    aadhaar_id_number = models.CharField(max_length=12, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    mother_name = models.CharField(max_length=50, blank=True, null=True)
    father_aadhaar_id_number = models.CharField(max_length=12, blank=True, null=True)
    mother_aaadhaar_id_number = models.CharField(max_length=12, blank=True, null=True)
    father_occupation = models.CharField(max_length=50, default="Not Specified")
    mother_occuption = models.CharField(max_length=50, default='Housewife')
    age = models.IntegerField(validators=[MinValueValidator(4, "Can only add students above 4 years of age")], blank=True)
    is_age_appropriate = models.BooleanField(default=False)
    age_appropiation_reason = models.TextField(blank=True, null=True)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE, blank=False, null=False, default="Rural")
    religion = models.CharField(max_length=50, blank=True, null=True)
    cast = models.CharField(max_length=20, choices=CAST, blank=False, null=False, default="General")
    belong_to_bpl = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    current_enrolled_type = models.CharField(max_length=20, choices=CURRENT_STATUS_STUDENT, blank=False, null=False, default="School")
    current_status = models.CharField(max_length=50, blank=True, default="Studying", choices=CURRENT_STATUS_STUDENT)
    
    def save(self, *args, **kwargs):
        day = self.date_of_birth.day
        birth_month = self.date_of_birth.month
        birth_year = self.date_of_birth.year
        current_date = datetime.now()
        
        if current_date.month < birth_month:
            self.age = current_date.year - birth_year - 1
        elif current_date.month == birth_month:
            if current_date.day < day:
                self.age = current_date.year - birth_year - 1
            else:
                self.age = current_date.year - birth_year
        else:
            self.age = current_date.year - birth_year
        
        with transaction.atomic():
            username = self.first_name+self.pin_code+self.father_aadhaar_id_number
            password = f"{self.first_name}{self.pin_code}"
            try:
                self.user == None
            except Exception:
                user = get_user_model().objects.create_user(username=username, password=password)
                username = f"{self.registered_year%100}{(10-len(str(user.pk)))*'0'}{user.pk}"
                user.username = username
                self.id = username
                self.user = user
                user.save()
        
        super().save(*args, **kwargs)        
        
        
    def __str__(self):
        return self.user.username   

   
class InstituteAdmin(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institute_admin')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='institute_admin', blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            username = self.institute.institute_id
            password = f"{self.institute.established_year}{self.institute.pincode}"
            try:
                self.user == None
            except Exception as e:
                user = get_user_model().objects.create_user(username=username, password=password)
                user.is_staff = True
                user.save()
                self.user = user
                    
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.institute.institute_id
    

class CentralEducationDepartment(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='central_edu', blank=True)
    username = models.CharField(max_length=250, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            username = f"edu_central"
            try:
                self.user
            except Exception as e:
                user = get_user_model().objects.create_superuser(username=username, password=username)
                self.user = user
                self.username = username
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class StateEducationDepartment(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='state_edu', blank=True)
    username = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=5, choices=STATES, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            username = f"edu_{self.state.lower()}"
            try:
                self.user
            except Exception as e:
                user = get_user_model().objects.create_user(username=username, password=username)
                user.is_staff = True
                user.save()
                self.user = user
                self.username = username
                
            super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.username
    
    
class DistrictEducationDepartment(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='district_edu', blank=True)
    username = models.CharField(max_length=250, blank=True)
    state = models.CharField(max_length=5, choices=STATES)
    district = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('state', 'district')
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            username = f"edu_{self.state.lower()}_{self.district.lower()}"
            try:
                self.user
            except Exception as e:
                user = get_user_model().objects.create_user(username=username, password=username)
                user.is_staff = True
                user.save()
                self.user = user
                self.username = username
                
            super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.user.delete()
            super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.username
    
    
@receiver(post_delete, sender=Student)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
@receiver(post_delete, sender=InstituteAdmin)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
@receiver(post_delete, sender=CentralEducationDepartment)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
@receiver(post_delete, sender=StateEducationDepartment)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
@receiver(post_delete, sender=DistrictEducationDepartment)
def delete_user(sender, instance, **kwargs):
    instance.user.delete()
    
    
    
class ResetOTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        subject = "Reset Password."
        message = f"OTP for resetting your password is {self.otp} for username {self.user.username}."
        receiver_mail = self.user.email
        
        try:
            send_mail(subject=subject, message=message, recipient_list=[receiver_mail], from_email="reset.slcm@edu.com")
        except Exception as e:
            pass
        