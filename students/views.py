from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .models import Student
from .forms import StudentForm


def teacher_or_admin(user):
    return user.role in ('admin', 'teacher')


@method_decorator(login_required, name='dispatch')
class StudentListView(View):
    def get(self, request):
        qs = Student.objects.filter(is_active=True)
        cls = request.GET.get('class')
        sec = request.GET.get('section')
        q = request.GET.get('q')
        if cls:
            qs = qs.filter(student_class=cls)
        if sec:
            qs = qs.filter(section=sec)
        if q:
            qs = qs.filter(first_name__icontains=q) | qs.filter(last_name__icontains=q) | qs.filter(roll_number__icontains=q)
        return render(request, 'students/list.html', {'students': qs})


@method_decorator(login_required, name='dispatch')
class StudentDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, 'students/detail.html', {'student': student})


@method_decorator(login_required, name='dispatch')
class StudentCreateView(View):
    def get(self, request):
        if not teacher_or_admin(request.user):
            return redirect('student_list')
        return render(request, 'students/form.html', {'form': StudentForm(), 'title': 'Add Student'})

    def post(self, request):
        if not teacher_or_admin(request.user):
            return redirect('student_list')
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
        return render(request, 'students/form.html', {'form': form, 'title': 'Add Student'})


@method_decorator(login_required, name='dispatch')
class StudentUpdateView(View):
    def get(self, request, pk):
        if not teacher_or_admin(request.user):
            return redirect('student_list')
        student = get_object_or_404(Student, pk=pk)
        return render(request, 'students/form.html', {'form': StudentForm(instance=student), 'title': 'Edit Student'})

    def post(self, request, pk):
        if not teacher_or_admin(request.user):
            return redirect('student_list')
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated.')
            return redirect('student_detail', pk=pk)
        return render(request, 'students/form.html', {'form': form, 'title': 'Edit Student'})


@method_decorator(login_required, name='dispatch')
class StudentDeleteView(View):
    def post(self, request, pk):
        if not request.user.is_admin():
            return redirect('student_list')
        student = get_object_or_404(Student, pk=pk)
        student.is_active = False
        student.save()
        messages.success(request, 'Student removed.')
        return redirect('student_list')
