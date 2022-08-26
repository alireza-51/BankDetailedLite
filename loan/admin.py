from django.contrib import admin
from .models import Loan, Payment

admin.site.register([Loan, Payment])
