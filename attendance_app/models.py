from django.db import models
from students.models import Student


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('holiday', 'Holiday'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    marked_by = models.CharField(max_length=100, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.roll_number} | {self.date} | {self.status}"


class QRAttendanceSession(models.Model):
    student_class = models.CharField(max_length=5)
    section = models.CharField(max_length=5)
    date = models.DateField()
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"QR Session {self.student_class}{self.section} - {self.date}"
