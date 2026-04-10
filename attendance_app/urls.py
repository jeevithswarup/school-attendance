from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance_list'),
    path('mark/', views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path('student/<int:pk>/', views.StudentAttendanceView.as_view(), name='student_attendance'),
    path('qr/generate/', views.QRGenerateView.as_view(), name='qr_generate'),
    path('qr-scan/<str:token>/', views.QRScanView.as_view(), name='qr_scan'),
]
