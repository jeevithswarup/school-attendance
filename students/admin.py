from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'first_name', 'last_name', 'student_class', 'section', 'is_active']
    list_filter = ['student_class', 'section', 'gender', 'is_active']
    search_fields = ['roll_number', 'first_name', 'last_name']
