from django.db import models
from students.models import Student


EXAM_CHOICES = [
    ('unit1', 'Unit Test 1'),
    ('unit2', 'Unit Test 2'),
    ('midterm', 'Mid Term'),
    ('final', 'Final Exam'),
]

GRADE_MAP = [
    (90, 'A+'), (80, 'A'), (70, 'B+'), (60, 'B'),
    (50, 'C'), (40, 'D'), (0, 'F')
]


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    academic_year = models.CharField(max_length=10, default='2024-25')

    def percentage(self):
        return round((float(self.marks_obtained) / float(self.max_marks)) * 100, 1)

    def grade(self):
        pct = self.percentage()
        for threshold, grade in GRADE_MAP:
            if pct >= threshold:
                return grade
        return 'F'

    def __str__(self):
        return f"{self.student.roll_number} | {self.subject.code} | {self.exam_type}"

    class Meta:
        unique_together = ('student', 'subject', 'exam_type', 'academic_year')
        ordering = ['subject', 'exam_type']
