from django.contrib import admin
from .models import TransferCertificate, Attendance, Enrollement, StudentCource, StudentSubject, StudentStreamEnrollment, StudentSchoolData, Stream, Cource, Subject

# Register your models here.

admin.site.register([TransferCertificate, Attendance, Enrollement, 
                     Stream, Cource, Subject,
                     StudentCource, StudentSubject, StudentStreamEnrollment, 
                    #  StudentSchoolData
                     ])
