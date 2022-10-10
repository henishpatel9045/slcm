from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from custom_users.model_choices import ENROLLMENT_TYPES, STUDENT_STREAM_STAUS
from entities.models import College, School

# Create your models here.
class TransferCertificate(models.Model):
    transfer_id = models.CharField(max_length=100, 
                                   unique=True, blank=True)
    student = models.ForeignKey('custom_users.Student', 
                                on_delete=models.CASCADE, 
                                related_name='transfer_certificate')
    generated_by = models.ForeignKey('entities.Institute', 
                                     on_delete=models.CASCADE, 
                                     related_name='parent_transfer_certificate')
    used_by = models.ForeignKey('entities.Institute', 
                                on_delete=models.CASCADE, 
                                related_name='transfer_certificate', 
                                blank=True, null=True)
    current_standard = models.IntegerField(default=1, 
                                           validators=[MinValueValidator(1), 
                                                       MaxValueValidator(12)])
    paid_all_fees = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)
    date_of_admission = models.DateField(blank=True)
    should_promote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.transfer_id:
            self.transfer_id = f'TC{timezone.now().year % 100}{self.student.pk}{self.generated_by.pk}'
        super().save(*args, **kwargs)
        
        
class Attendance(models.Model):
    student = models.ForeignKey('custom_users.Student', 
                                on_delete=models.CASCADE, 
                                related_name='attendance')
    institute = models.ForeignKey('entities.Institute', 
                                  on_delete=models.CASCADE, 
                                  related_name='attendance')
    month = models.IntegerChoices('month', 
                                  'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC')
    year = models.IntegerField(default=2021, 
                               validators=[MinValueValidator(1800), 
                                           MaxValueValidator(2100)])
    attended_days = models.IntegerField(default=0, 
                                        validators=[MinValueValidator(0),
                                                    MaxValueValidator(31)])
    working_days = models.IntegerField(default=0, 
                                       validators=[MinValueValidator(0), 
                                                   MaxValueValidator(31)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'institute')


class Enrollement(models.Model):
    student = models.ForeignKey('custom_users.Student', 
                                on_delete=models.CASCADE, 
                                related_name='enrollement')
    institute = models.ForeignKey('entities.Institute',
                                  on_delete=models.CASCADE, 
                                  related_name='enrollement')
    current_year = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=STUDENT_STREAM_STAUS, default='In Progress')
    enrolled_via = models.CharField(max_length=100, blank=True, null=True, choices=ENROLLMENT_TYPES, default='New Registration')
    transfer_certificate = models.ForeignKey('operations.TransferCertificate', 
                                             on_delete=models.DO_NOTHING, 
                                             related_name='enrollement', 
                                             blank=True, null=True)
    date_of_admission = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'institute', 'current_year')


class StudentStreamEnrollment(models.Model):
    enrollment = models.ForeignKey('operations.Enrollement',on_delete=models.CASCADE, related_name='stream_enrollment')
    student = models.ForeignKey('custom_users.Student', on_delete=models.CASCADE, related_name='stream_enrollment')
    stream = models.ForeignKey('operations.Stream', on_delete=models.CASCADE, related_name='stream_enrollment')

    def __str__(self):
        return self.student.id + " " + self.stream.name

class Stream(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='stream')
    total_years = models.IntegerField(default=4, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('name', 'college')
        
    def __str__(self):
        return self.name


class StudentSchoolData(models.Model):
    student = models.ForeignKey('custom_users.Student', on_delete=models.CASCADE, related_name='current_stream')
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='current_stream', blank=True, null=True)
    curent_year = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=100, choices=STUDENT_STREAM_STAUS, default='In Progress')
    

class Cource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='cources')
    years = models.IntegerField(default=1,
                                validators=[MinValueValidator(0)])
    months = models.IntegerField(default=0,
                                 validators=[MinValueValidator(0),
                                             MaxValueValidator(11)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class StudentCource(models.Model):
    student = models.ForeignKey('custom_users.Student', on_delete=models.CASCADE, related_name='student_cources')
    cources = models.ForeignKey(Cource, on_delete=models.CASCADE)
    enrolled_year = models.IntegerField(default=2021,validators=[MinValueValidator(1800),MaxValueValidator(2100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'cources', 'enrolled_year')
        

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    school = models.ForeignKey(School, 
                                on_delete=models.CASCADE,
                                related_name='cources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class StudentSubject(models.Model):
    student = models.ForeignKey('custom_users.Student', on_delete=models.CASCADE, related_name='student_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_subjects')
    standard = models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(12)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'subject', 'standard')