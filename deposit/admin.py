from django.contrib import admin
from .models import Deposit, Withdrawal

class DepositAdmin(admin.ModelAdmin):
    list_display = ['customer', 'account_no']
    fields = ['customer', 'branch', 'balance', 'account_no']
    readonly_fields = ['account_no']

admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal)