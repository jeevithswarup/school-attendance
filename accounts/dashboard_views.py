from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from students.models import Student
from attendance_app.models import Attendance
from fees.models import FeePayment
from marks.models import Mark
from django.utils import timezone


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user = request.user
        context = {'user': user}

        if user.is_admin():
            context.update({
                'total_students': Student.objects.count(),
                'total_teachers': user.__class__.objects.filter(role='teacher').count(),
                'today_present': Attendance.objects.filter(
                    date=timezone.now().date(), status='present').count(),
                'pending_fees': FeePayment.objects.filter(status='pending').count(),
            })
            return render(request, 'dashboards/admin.html', context)

        elif user.is_teacher():
            context.update({
                'total_students': Student.objects.count(),
                'today_present': Attendance.objects.filter(
                    date=timezone.now().date(), status='present').count(),
            })
            return render(request, 'dashboards/teacher.html', context)

        elif user.is_student():
            try:
                student = Student.objects.get(user=user)
                context.update({
                    'student': student,
                    'attendance_pct': student.attendance_percentage(),
                    'recent_marks': Mark.objects.filter(student=student).order_by('-id')[:5],
                    'fee_status': FeePayment.objects.filter(student=student).order_by('-created_at')[:3],
                })
            except Student.DoesNotExist:
                pass
            return render(request, 'dashboards/student.html', context)

        elif user.is_parent():
            students = Student.objects.filter(parent_user=user)
            context['students'] = students
            return render(request, 'dashboards/parent.html', context)

        return redirect('login')
