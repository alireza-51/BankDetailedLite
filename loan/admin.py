from django.contrib import admin
from .models import Loan, Payment

class LoanAdmin(admin.ModelAdmin):
    list_display = ['customer', 'loan_no']
    fields = ['customer', 'branch', 'amount', 'loan_no']
    readonly_fields = ['loan_no']

admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment)
