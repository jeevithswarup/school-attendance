from django.contrib import admin
from .models import FeePayment, FeeStructure

admin.site.register(FeeStructure)

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_due', 'amount_paid', 'status', 'payment_date']
    list_filter = ['status']
    search_fields = ['student__roll_number', 'receipt_number']
