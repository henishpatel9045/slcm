from decimal import Decimal
from rest_framework import views, status
from rest_framework.response import Response
from custom_users.models import Student

from django.db import transaction

from operations.serializers import EnrollmentSerializers, TCSerializer
from .models import Enrollement, TransferCertificate
from django.contrib.auth import get_user_model


# Create your views here.

class StudentInstituteAPI(views.APIView):
    def get(self, request, pk):
        user = self.request.user
        student = Student.objects.get(id=pk)
        qs = Enrollement.objects.select_related("institute").filter(student=student).order_by('date_of_admission')
        res =  EnrollmentSerializers(qs, many=True, read_only=True)
        
        if len(res.data) <= 0:
            return Response({"detail": "Student hasn't enrolled in institutes yet."})
        
        return Response(res.data, status=status.HTTP_200_OK)
    

def generate_tc(request):
    conflicted_student = []
    conflict_message = []
    success_message = []
    
    user = request.data.user
    current_enrollment = Enrollement.objects.filter(is_active=True, student__user=user)
    sid = request.data.get("student_id")
    student = Student.objects.get(id=sid)
    if not current_enrollment.exists():
        return Response({"detail": "Selected user hasn't currently enrolled in any institute.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
    
    exists_tc = TransferCertificate.objects.filter(student__user=user, used_by__isnull=False)
    
    if exists_tc.exists():
        exists_tc = exists_tc.first()
        return Response({"detail": "Selected user hasn't currently enrolled in any institute.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        
    # paid_all_fees = request.data.get("paid_all_fees", True)
    # remaining_fees = request.data.get("remaining_fees", 0.0)
    current_standard = current_institute.current_year
    current_institute = current_institute.institute
    should_promoted = request.data.get("should_promoted", False)
    comment = request.data.get("comment","")
    
    created_by = user.institute_admin.institute
    
    tc = TransferCertificate()
    tc.student = student
    tc.generated_by = created_by
    tc.current_standard = current_standard
    tc.date_of_admission = current_enrollment.date_of_admission
    tc.should_promote = should_promoted
    # tc.paid_all_fees = paid_all_fees
    # tc.remaining_fees = Decimal.quantize(remaining_fees, Decimal("1.00"))
    tc.comment = comment
    with transaction.atomic():
        current_enrollment.is_active = False
        current_enrollment.save()
        tc.save()
    
    success_message.append({"detail": "Transfer certificate successfully generated.",
                             "student": student.id,
                             "transfer_id": tc.transfer_id,
                             "status": True})
      

    
class GenerateTCView(views.APIView):
    def get(self, request):
        user = self.request.user
        
        if hasattr(user, 'app_user'):
            qs = TransferCertificate.objects.filter(student__user=user)
        else:
            qs = TransferCertificate.objects.all()
        
        tc_id = self.kwargs.get("pk")
        if not tc_id:
            serializer = TCSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    
    
    def post(self, request):
        try:
            user = request.data.user
            current_enrollment = Enrollement.objects.filter(is_active=True, student__user=user)
            sid = request.data.get("student_id")
            student = Student.objects.get(id=sid)
            if not current_enrollment.exists():
                return Response({"detail": "Selected user hasn't currently enrolled in any institute.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
            
            exists_tc = TransferCertificate.objects.filter(student__user=user, used_by__isnull=False)
            
            if exists_tc.exists():
                exists_tc = exists_tc.first()
                return Response({"detail": "Selected user hasn't currently enrolled in any institute.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
                
            # paid_all_fees = request.data.get("paid_all_fees", True)
            # remaining_fees = request.data.get("remaining_fees", 0.0)
            current_standard = current_institute.current_year
            current_institute = current_institute.institute
            should_promoted = request.data.get("should_promoted", False)
            comment = request.data.get("comment","")
            
            created_by = user.institute_admin.institute
            
            tc = TransferCertificate()
            tc.student = student
            tc.generated_by = created_by
            tc.current_standard = current_standard
            tc.date_of_admission = current_enrollment.date_of_admission
            tc.should_promote = should_promoted
            # tc.paid_all_fees = paid_all_fees
            # tc.remaining_fees = Decimal.quantize(remaining_fees, Decimal("1.00"))
            tc.comment = comment
            with transaction.atomic():
                current_enrollment.is_active = False
                current_enrollment.save()
                tc.save()
            
            return Response({"detail": "Transfer certificate successfully generated.",
                                    "student": student.id,
                                    "transfer_id": tc.transfer_id,
                                    "status": True}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"detail": str(e.args[0]), "status": False}, status=status.HTTP_400_BAD_REQUEST)
        
        
def generate_bulk_tc(users):
    conflicted_student = []
    conflict_message = []
    success_message = []
    
    for i, request in enumerate(users):
        print(request)       
        user = request.get("user")
        student = request.get("student")
        current_enrollment = Enrollement.objects.filter(is_active=True, student=student)
        print(current_enrollment)
        if not current_enrollment.exists():
            print(current_enrollment)
            conflict_message.append("Selected user hasn't currently enrolled in any institute.")
            continue
        
        current_enrollment = current_enrollment.first()
        current_institute = current_enrollment.institute
        exists_tc = TransferCertificate.objects.filter(student=student, used_by__isnull=False)
        
        if exists_tc.exists():
            exists_tc = exists_tc.first()
            conflicted_student.append(student.id)
            conflict_message.append(f"Transfer certificate for {student.id} already exists with id {exists_tc.transfer_id}.")
            continue
        
        # paid_all_fees = request.get("paid_all_fees", True)
        # remaining_fees = request.get("remaining_fees", 0.0)
        current_standard = current_enrollment.current_year
        
        should_promoted = request.get("should_promoted", False)
        comment = request.get("comment","")
        
        created_by = user.institute_admin.institute
        
        tc = TransferCertificate()
        tc.student = student
        tc.generated_by = created_by
        tc.current_standard = current_standard
        tc.date_of_admission = current_enrollment.date_of_admission
        tc.should_promote = should_promoted
        # tc.paid_all_fees = paid_all_fees
        # tc.remaining_fees = Decimal.quantize(remaining_fees, Decimal("1.00"))
        tc.comment = comment
        with transaction.atomic():
            current_enrollment.is_active = False
            current_enrollment.save()
            tc.save()
        
        success_message.append({"detail": "Transfer certificate successfully generated.",
                           "student": student.id,
                             "transfer_id": tc.transfer_id,
                             "status": True})
            
    return success_message, conflicted_student, conflict_message

            
class GenerateBulkTCView(views.APIView):
    def post(self, request):
        print(request.data)
        data = request.data.get("tc_data")
        
        print(request.data)
        if not data:
            return Response({"detail": "No data provided in body.", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        
        for d in data:
            d['user'] = request.user
            d['student'] = Student.objects.get(id=d.get("student_id"))
                
        success_message, conflicted_student, conflict_message = generate_bulk_tc(data)
        
        return Response({
            "success_message": success_message,
            "conflicts": conflict_message,
        }, status=status.HTTP_200_OK)
        
        
        
class DashboardAPI(views.APIView):
    
    def get(self, request):
        user = request.user
        if hasattr(user, 'institute_admin'):
            institute = user.institute_admin.institute
            enroll_qs = Enrollement.objects.filter(institute=institute)
            tc_qs = TransferCertificate.objects.filter(generated_by=institute)
        elif hasattr(user, 'central_edu'):
            enroll_qs = Enrollement.objects.all()
            tc_qs = TransferCertificate.objects.all()
        elif hasattr(user, 'state_edu'):
            enroll_qs = Enrollement.objects.filter(institute__state=user.state_edu.state)
            tc_qs = TransferCertificate.objects.filter(institute__state=user.state_edu.state)
            
        else:
            enroll_qs = Enrollement.objects.filter(institute__district=user.state_edu.district)
            tc_qs = TransferCertificate.objects.filter(institute__district=user.state_edu.district)
            
        current_streangth = enroll_qs.filter(is_active=True).count()
        total_students_enrolled = enroll_qs.filter(institute=institute).count()
        total_passout = enroll_qs.filter(institute=institute, status="Completed").count()
        total_transfer_generated = tc_qs.filter(generated_by=institute).count()
        total_new_admission = enroll_qs.filter(enrolled_via="New Registration", institute=institute).count()
        total_admission_through_tc = total_students_enrolled - total_new_admission
        
        return Response({
            "current_streangth": current_streangth,
            "total_students_enrolled": total_students_enrolled,
            "total_passout": total_passout,
            "total_transfer_generated": total_transfer_generated,
            "total_new_admission": total_new_admission,
            "total_admission_through_tc": total_admission_through_tc
        }, status=status.HTTP_200_OK)
    
    
    
    

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  

# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None



class SendMail(views.APIView):
    def get(self, request, tc_id):
        print(tc_id)
        qs = TransferCertificate.objects.get(transfer_id=tc_id)
        print(qs)
        context = {
            'student_id': qs.student.id,
            'student_name': f"{qs.student.first_name} {qs.student.middle_name} {qs.student.last_name}",
            'institute_id': qs.generated_by.institute_id,
            'institute_name': qs.generated_by.name,
            'tc_id': qs.transfer_id,
            'generated_by_id': qs.generated_by.institute_id,
            'used_by_id': qs.used_by.institute_id if qs.used_by else None,
            'joining_date': qs.date_of_admission,
            'leave_date': qs.created_at,
            'current_standard': qs.current_standard,
            'should_promote': qs.should_promote
        }

        try:
            response = html_to_pdf("tc.html", context)
            return response
        except Exception as e:
            return Response({"detail": "Error occurred.", "error": str(e.args[0])}, status=status.HTTP_400_BAD_REQUEST)
        