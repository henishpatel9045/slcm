from import_export import resources
from .models import Student

class StudentResources(resources.ModelResource):
    
    class Meta:
        model = Student
        fields = ['id',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'gender',
                    'address_line',
                    'city',
                    'pin_code',
                    'township',
                    'district',
                    'state',
                    'phone',
                    'father_phone',
                    'mother_phone',
                    'email',
                    'registered_year',
                    'date_of_birth',
                    'aadhaar_id_number',
                    'mother_tongue',
                    'father_name',
                    'mother_name',
                    'father_aadhaar_id_number',
                    'mother_aadhaar_id_number',
                    'father_occupation',
                    'mother_occuption',
                    'age',
                    'address_type',
                    'religion',
                    'caste',
                    'active',
                  ]
        export_order = ['id',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'gender',
                    'address_line',
                    'city',
                    'pin_code',
                    'township',
                    'district',
                    'state',
                    'phone',
                    'father_phone',
                    'mother_phone',
                    'email',
                    'registered_year',
                    'date_of_birth',
                    'aadhaar_id_number',
                    'mother_tongue',
                    'father_name',
                    'mother_name',
                    'father_aadhaar_id_number',
                    'mother_aadhaar_id_number',
                    'father_occupation',
                    'mother_occuption',
                    'age',
                    'address_type',
                    'religion',
                    'caste',
                    'active',
                  ]
        
    