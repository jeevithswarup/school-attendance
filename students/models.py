from django.db import models
from accounts.models import User


CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(1, 13)]
SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='student_profile')
    parent_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='children', limit_choices_to={'role': 'parent'})
    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    student_class = models.CharField(max_length=5, choices=CLASS_CHOICES)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def attendance_percentage(self):
        from attendance_app.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status='present').count()
        return round((present / total) * 100, 1)

    def __str__(self):
        return f"{self.roll_number} - {self.full_name()} ({self.student_class}{self.section})"

    class Meta:
        ordering = ['student_class', 'section', 'roll_number']
