from django.test import TestCase
from deposit.models import Deposit, Withdrawal
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
        return super().setUp()

    def test_has_valid_account_no(self):
        self.assertIsNotNone(self.deposit.account_no)
        self.assertRegex(self.deposit.account_no, r'^[1-9][0-9]{9,14}$')

class TestWithrawal(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            national_no = '2587413690',
            first_name = 'test',
            last_name = 'test',
            username = 'user',
            address = 'test...',
            typ = User.Typ.CUSTOMER
        )
        self.branch = Branch.objects.create(name='test', city='test', address='test...')
        self.deposit = Deposit.objects.create(
            customer = self.user,
            branch = self.branch,
            balance = 1000
        )
        return super().setUp()
    
    def test_withdraw_deposit(self):
        withdraw = Withdrawal.objects.create(
            user = self.user,
            deposit = self.deposit,
            amount = 500,
            typ = Withdrawal.Typ.WITHDRAW
        )
        self.assertEqual(self.deposit.balance, 500)

        with self.assertRaises(ValueError):
            withdraw = Withdrawal.objects.create(
                user = self.user,
                deposit = self.deposit,
                amount = 5000,
                typ = Withdrawal.Typ.WITHDRAW
            )

        deposit = Withdrawal.objects.create(
            user = self.user,
            deposit = self.deposit,
            amount = 500,
            typ = Withdrawal.Typ.DEPOSIT
        )
        self.assertEqual(self.deposit.balance, 1000)
