from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from .models import Mark, Subject
from .forms import MarkForm, SubjectForm
from students.models import Student

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


@method_decorator(login_required, name='dispatch')
class MarkListView(View):
    def get(self, request):
        if request.user.role == 'student':
            try:
                student = Student.objects.get(user=request.user)
                marks = Mark.objects.filter(student=student).select_related('subject')
            except Student.DoesNotExist:
                marks = Mark.objects.none()
                student = None
            return render(request, 'marks/list.html', {'marks': marks, 'student': student})
        marks = Mark.objects.select_related('student', 'subject').all()
        return render(request, 'marks/list.html', {'marks': marks})


@method_decorator(login_required, name='dispatch')
class MarkCreateView(View):
    def get(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('mark_list')
        return render(request, 'marks/form.html', {'form': MarkForm(), 'title': 'Add Mark'})

    def post(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('mark_list')
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mark saved.')
            return redirect('mark_list')
        return render(request, 'marks/form.html', {'form': form, 'title': 'Add Mark'})


@method_decorator(login_required, name='dispatch')
class MarkUpdateView(View):
    def get(self, request, pk):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('mark_list')
        mark = get_object_or_404(Mark, pk=pk)
        return render(request, 'marks/form.html', {'form': MarkForm(instance=mark), 'title': 'Edit Mark'})

    def post(self, request, pk):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('mark_list')
        mark = get_object_or_404(Mark, pk=pk)
        form = MarkForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mark updated.')
            return redirect('mark_list')
        return render(request, 'marks/form.html', {'form': form, 'title': 'Edit Mark'})


@method_decorator(login_required, name='dispatch')
class ReportCardView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        marks = Mark.objects.filter(student=student).select_related('subject').order_by('subject__name', 'exam_type')
        return render(request, 'marks/report_card.html', {
            'student': student,
            'marks': marks,
            'pct': student.attendance_percentage(),
        })


@method_decorator(login_required, name='dispatch')
class ReportCardPDFView(View):
    def get(self, request, pk):
        if not REPORTLAB_AVAILABLE:
            messages.error(request, 'PDF generation requires reportlab. Install it with: pip install reportlab')
            return redirect('student_report_card', pk=pk)

        student = get_object_or_404(Student, pk=pk)
        marks = Mark.objects.filter(student=student).select_related('subject').order_by('subject__name')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_card_{student.roll_number}.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Header
        p.setFillColor(colors.HexColor('#1a237e'))
        p.rect(0, height - 80, width, 80, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont('Helvetica-Bold', 18)
        p.drawCentredString(width / 2, height - 35, 'SCHOOL MANAGEMENT SYSTEM')
        p.setFont('Helvetica', 12)
        p.drawCentredString(width / 2, height - 55, 'Student Report Card')

        # Student info
        p.setFillColor(colors.black)
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, height - 110, f'Name: {student.full_name}')
        p.drawString(50, height - 130, f'Roll No: {student.roll_number}')
        p.drawString(300, height - 110, f'Class: {student.student_class} - {student.section}')
        p.drawString(300, height - 130, f'Attendance: {student.attendance_percentage()}%')

        # Table header
        y = height - 170
        p.setFillColor(colors.HexColor('#e8eaf6'))
        p.rect(40, y - 5, width - 80, 20, fill=True, stroke=False)
        p.setFillColor(colors.black)
        p.setFont('Helvetica-Bold', 10)
        p.drawString(50, y, 'Subject')
        p.drawString(220, y, 'Exam')
        p.drawString(340, y, 'Marks')
        p.drawString(420, y, 'Max')
        p.drawString(480, y, 'Grade')

        y -= 25
        p.setFont('Helvetica', 10)
        for m in marks:
            p.drawString(50, y, m.subject.name[:25])
            p.drawString(220, y, m.get_exam_type_display())
            p.drawString(340, y, str(m.marks_obtained))
            p.drawString(420, y, str(m.max_marks))
            p.drawString(480, y, m.grade())
            y -= 20
            if y < 60:
                p.showPage()
                y = height - 60

        p.setFont('Helvetica-Oblique', 9)
        p.setFillColor(colors.grey)
        p.drawCentredString(width / 2, 30, 'Generated by SchoolSMS')
        p.save()
        return response


@method_decorator(login_required, name='dispatch')
class SubjectListView(View):
    def get(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('mark_list')
        subjects = Subject.objects.all()
        return render(request, 'marks/subjects.html', {'subjects': subjects})


@method_decorator(login_required, name='dispatch')
class SubjectCreateView(View):
    def get(self, request):
        if request.user.role not in ('admin',):
            return redirect('subject_list')
        return render(request, 'marks/subject_form.html', {'form': SubjectForm(), 'title': 'Add Subject'})

    def post(self, request):
        if request.user.role not in ('admin',):
            return redirect('subject_list')
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added.')
            return redirect('subject_list')
        return render(request, 'marks/subject_form.html', {'form': form, 'title': 'Add Subject'})
