from django.db import models
from students.models import Student


class FeeStructure(models.Model):
    student_class = models.CharField(max_length=5)
    fee_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=10, default='2024-25')

    def __str__(self):
        return f"Class {self.student_class} - {self.fee_type} - ₹{self.amount}"


class FeePayment(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('paid', 'Paid'), ('partial', 'Partial')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def balance(self):
        return self.amount_due - self.amount_paid

    def __str__(self):
        return f"{self.student.roll_number} - {self.status} - ₹{self.amount_due}"

    class Meta:
        ordering = ['-created_at']
