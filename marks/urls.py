from django.urls import path
from . import views

urlpatterns = [
    path('', views.MarkListView.as_view(), name='mark_list'),
    path('add/', views.MarkCreateView.as_view(), name='mark_add'),
    path('<int:pk>/edit/', views.MarkUpdateView.as_view(), name='mark_edit'),
    path('student/<int:pk>/report/', views.ReportCardView.as_view(), name='student_report_card'),
    path('student/<int:pk>/report/pdf/', views.ReportCardPDFView.as_view(), name='report_card_pdf'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
]
