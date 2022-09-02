from django.test import TestCase
from .models import Deposit, Withdrawal
from branch.models import Branch
from django.contrib.auth import get_user_model

User = get_user_model()

class TestDeposit(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            national_no = '9876543210',
            first_name = 'test',
            last_name = 'test',
            username = 'test',
            address = 'test...',
            typ = User.Typ.CUSTOMER
        )
        self.branch = Branch.objects.create(name='test', city='test', address='test...')
        self.deposit = Deposit.objects.create(
            customer = self.user,
            branch = self.branch,
            balance = 1000
        )

    def test_has_valid_account_no(self):
        self.assertIsNotNone(self.deposit.account_no)
        self.assertRegex(self.deposit.account_no, r'^[1-9][0-9]{9,14}$')
