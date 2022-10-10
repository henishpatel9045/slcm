from django.contrib import admin
from .models import Student, InstituteAdmin, CentralEducationDepartment, StateEducationDepartment, DistrictEducationDepartment

# Register your models here.

admin.site.title = "SLCM Dashboard"

admin.site.register(Student)
admin.site.register(InstituteAdmin)
admin.site.register(CentralEducationDepartment)
admin.site.register(StateEducationDepartment)
admin.site.register(DistrictEducationDepartment)
