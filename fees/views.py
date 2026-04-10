from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .models import FeePayment, FeeStructure
from .forms import FeePaymentForm, FeeStructureForm
from students.models import Student


@method_decorator(login_required, name='dispatch')
class FeeListView(View):
    def get(self, request):
        if request.user.role == 'student':
            try:
                student = Student.objects.get(user=request.user)
                payments = FeePayment.objects.filter(student=student)
            except Student.DoesNotExist:
                payments = FeePayment.objects.none()
        else:
            payments = FeePayment.objects.select_related('student').all()
        return render(request, 'fees/list.html', {'payments': payments})


@method_decorator(login_required, name='dispatch')
class FeeCreateView(View):
    def get(self, request):
        if request.user.role not in ('admin',):
            return redirect('fee_list')
        return render(request, 'fees/form.html', {'form': FeePaymentForm(), 'title': 'Add Fee Record'})

    def post(self, request):
        if request.user.role not in ('admin',):
            return redirect('fee_list')
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record added.')
            return redirect('fee_list')
        return render(request, 'fees/form.html', {'form': form, 'title': 'Add Fee Record'})


@method_decorator(login_required, name='dispatch')
class FeeUpdateView(View):
    def get(self, request, pk):
        if request.user.role not in ('admin',):
            return redirect('fee_list')
        payment = get_object_or_404(FeePayment, pk=pk)
        return render(request, 'fees/form.html', {'form': FeePaymentForm(instance=payment), 'title': 'Update Fee'})

    def post(self, request, pk):
        if request.user.role not in ('admin',):
            return redirect('fee_list')
        payment = get_object_or_404(FeePayment, pk=pk)
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee updated.')
            return redirect('fee_list')
        return render(request, 'fees/form.html', {'form': form, 'title': 'Update Fee'})


@method_decorator(login_required, name='dispatch')
class StudentFeeView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        payments = FeePayment.objects.filter(student=student)
        return render(request, 'fees/student_fees.html', {'student': student, 'payments': payments})
