from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from branch.models import Branch
from utils.incremental_id_picker import increment_id_number

User = get_user_model()

class Deposit(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    account_no = models.CharField(verbose_name="Account number", max_length=15,
        null=False, blank=False)
    balance = models.DecimalField(max_digits=20, decimal_places=1, default=0)

    def __str__(self) -> str:
        return '{}'.format(self.account_no)

    def save(self, *args, **kwargs) -> None:
        if not self.account_no:
            self.account_no = increment_id_number(Deposit, 'account_no')
        return super().save(*args, **kwargs)

class Withdrawal(models.Model):
    class Typ(models.IntegerChoices):
        DEPOSIT = 0, _('Deposit')
        WITHDRAW = 1, _('Withdraw')
    
    deposit = models.OneToOneField(Deposit, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=1)
    typ = models.IntegerField(choices=Typ.choices, null=False, blank=False)
    datetime = models.DateTimeField()

    def __str__(self) -> str:
        return '{} :{}'.format(self.deposit.account_no, self.amount)

    def save(self, *args, **kwargs) -> None:
        # update the balance in the deposit account
        return super().save(*args, **kwargs)