import uuid
import io
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from students.models import Student
from .models import Attendance, QRAttendanceSession
from .forms import AttendanceFilterForm, QRSessionForm


@method_decorator(login_required, name='dispatch')
class AttendanceListView(View):
    def get(self, request):
        form = AttendanceFilterForm(request.GET or None)
        date = timezone.now().date()
        students = Student.objects.filter(is_active=True)

        if form.is_valid():
            date = form.cleaned_data['date']
            cls = form.cleaned_data.get('student_class')
            sec = form.cleaned_data.get('section')
            if cls:
                students = students.filter(student_class=cls)
            if sec:
                students = students.filter(section=sec)

        attendance_map = {
            a.student_id: a for a in Attendance.objects.filter(date=date, student__in=students)
        }
        rows = [{'student': s, 'attendance': attendance_map.get(s.id)} for s in students]
        return render(request, 'attendance/list.html', {'form': form, 'rows': rows, 'date': date})


@method_decorator(login_required, name='dispatch')
class MarkAttendanceView(View):
    def get(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('attendance_list')
        form = AttendanceFilterForm(request.GET or None)
        date = timezone.now().date()
        students = Student.objects.filter(is_active=True)

        if form.is_valid():
            date = form.cleaned_data['date']
            cls = form.cleaned_data.get('student_class')
            sec = form.cleaned_data.get('section')
            if cls:
                students = students.filter(student_class=cls)
            if sec:
                students = students.filter(section=sec)

        return render(request, 'attendance/mark.html', {
            'form': form,
            'students': students,
            'date': date,
        })

    def post(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('attendance_list')

        from datetime import date as dt
        import re

        date_str = request.POST.get('date')
        date = dt.fromisoformat(date_str)

        # Parse roll numbers — split on commas, spaces, newlines
        raw = request.POST.get('present_rolls', '')
        present_rolls = set(r.strip().upper() for r in re.split(r'[\s,]+', raw) if r.strip())

        # Filter scope (class/section if provided)
        cls = request.POST.get('student_class', '')
        sec = request.POST.get('section', '')
        students = Student.objects.filter(is_active=True)
        if cls:
            students = students.filter(student_class=cls)
        if sec:
            students = students.filter(section=sec)

        present_count = 0
        absent_count = 0
        not_found = []

        # Validate that entered roll numbers actually exist in scope
        for roll in present_rolls:
            if not students.filter(roll_number__iexact=roll).exists():
                not_found.append(roll)

        if not_found:
            messages.warning(request, f'Roll numbers not found: {", ".join(not_found)}')

        # Mark all students in scope
        from notifications.emails import notify_absent, notify_late
        for student in students:
            status = 'present' if student.roll_number.upper() in present_rolls else 'absent'
            Attendance.objects.update_or_create(
                student=student, date=date,
                defaults={'status': status, 'marked_by': request.user.username}
            )
            if status == 'present':
                present_count += 1
            else:
                absent_count += 1
                notify_absent(student, date, marked_by=request.user.username)

        messages.success(request, f'Attendance saved — {present_count} present, {absent_count} absent.')
        return redirect('attendance_list')


@method_decorator(login_required, name='dispatch')
class StudentAttendanceView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        records = Attendance.objects.filter(student=student).order_by('-date')
        return render(request, 'attendance/student.html', {
            'student': student,
            'records': records,
            'pct': student.attendance_percentage()
        })


@method_decorator(login_required, name='dispatch')
class QRGenerateView(View):
    def get(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('attendance_list')
        return render(request, 'attendance/qr_generate.html', {'form': QRSessionForm()})

    def post(self, request):
        if request.user.role not in ('admin', 'teacher'):
            return redirect('attendance_list')
        form = QRSessionForm(request.POST)
        if form.is_valid():
            token = uuid.uuid4().hex
            session = QRAttendanceSession.objects.create(
                student_class=form.cleaned_data['student_class'],
                section=form.cleaned_data['section'],
                date=form.cleaned_data['date'],
                token=token,
            )
            qr_url = request.build_absolute_uri(f'/attendance/qr-scan/{token}/')
            img = qrcode.make(qr_url)
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return HttpResponse(buf, content_type='image/png')
        return render(request, 'attendance/qr_generate.html', {'form': form})


class QRScanView(View):
    def get(self, request, token):
        session = get_object_or_404(QRAttendanceSession, token=token, is_active=True)
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next=/attendance/qr-scan/{token}/')
        try:
            student = Student.objects.get(user=request.user)
            Attendance.objects.update_or_create(
                student=student, date=session.date,
                defaults={'status': 'present', 'marked_by': 'QR'}
            )
            messages.success(request, f'Attendance marked for {session.date}')
        except Student.DoesNotExist:
            messages.error(request, 'No student profile linked to your account.')
        return redirect('dashboard')
