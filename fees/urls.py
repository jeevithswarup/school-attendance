from django.urls import path
from . import views

urlpatterns = [
    path('', views.FeeListView.as_view(), name='fee_list'),
    path('add/', views.FeeCreateView.as_view(), name='fee_add'),
    path('<int:pk>/edit/', views.FeeUpdateView.as_view(), name='fee_edit'),
    path('student/<int:pk>/', views.StudentFeeView.as_view(), name='student_fees'),
]
