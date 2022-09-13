from django.db import models
from utils.incremental_id_picker import increment_id_number
from django.contrib.auth import get_user_model
from branch.models import Branch
from deposit.models import Deposit, Withdrawal

User = get_user_model()

class Loan(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    loan_no = models.CharField(verbose_name="Loan number", max_length=15,
        null=False, blank=False)
    amount = models.DecimalField(max_digits=20, decimal_places=1)

    def __str__(self) -> str:
        return '{}'.format(self.loan_no)

    def save(self, *args, **kwargs) -> None:
        deposit = Deposit.objects.filter(branch=self.branch, customer=self.customer)
        if not deposit:
            raise ValueError('User has no deposit in this branch')
        if not self.loan_no:
            self.loan_no = increment_id_number(Loan, 'loan_no', digit=8)
        return super().save(*args, **kwargs)

class Payment(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name='payments')
    withdraw  = models.OneToOneField(Withdrawal, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    def __str__(self) -> str:
        return '{} :{}'.format(self.loan_no, self.withdraw.amount)

    