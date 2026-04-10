from django.contrib import admin
from .models import Attendance, QRAttendanceSession


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date']
    search_fields = ['student__roll_number', 'student__first_name']


@admin.register(QRAttendanceSession)
class QRSessionAdmin(admin.ModelAdmin):
    list_display = ['student_class', 'section', 'date', 'is_active']
