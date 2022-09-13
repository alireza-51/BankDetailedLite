from django.test import TestCase

from deposit.models import Deposit
from loan.models import Loan, Payment
from branch.models import Branch
from django.contrib.auth import get_user_model

User = get_user_model()


class TestLoan(TestCase):
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
        # self.loan = Loan.objects.create(
        #     customer = self.user,
        #     branch = self.branch,
        #     amount = 1000
        # )

        return super().setUp()

    def test_loan(self):
        with self.assertRaises(ValueError):
            self.loan = Loan.objects.create(
                customer = self.user,
                branch = self.branch,
                amount = 1000
            )
        self.deposit = Deposit.objects.create(
            customer = self.user,
            branch = self.branch,
            balance = 1000
        )
        self.loan = Loan.objects.create(
            customer = self.user,
            branch = self.branch,
            amount = 1000
        )
        self.assertIsNotNone(self.loan.loan_no)
        self.assertRegex(self.loan.loan_no, r'^[1-9][0-9]{7,14}$')