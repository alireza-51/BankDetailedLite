from django.test import TestCase
from rest_framework import test, status
from loan.models import Loan, Payment
from django.contrib.auth import get_user_model
from deposit.models import Deposit
from branch.models import Branch
from loan.api.serializers import LoanSerializer

User = get_user_model()

class TestLoan(TestCase):
    def setUp(self) -> None:
        self.branch = Branch.objects.create(name='test', city='test', address='test...')

        self.customer, _ = User.objects.get_or_create(
            national_no = '1234567890',
            first_name = 'test',
            last_name = 'test',
            username = 'customer',
            address = 'test...',
            email='',
            typ = User.Typ.CUSTOMER
        )
        self.customer.set_password('test')
        self.customer.save()

        self.admin_user, _ = User.objects.get_or_create(
            national_no='9876543210',
            username='admin',
            first_name='test',
            last_name='test',
            address='test...',
            email='',
            typ=User.Typ.STAFF,
        )
        self.admin_user.set_password('test')
        self.admin_user.save()


        self.another_customer, _ = User.objects.get_or_create(
            national_no = '4567890123',
            first_name = 'test',
            last_name = 'test',
            username = 'anothercustomer',
            address = 'test...',
            email='',
            typ = User.Typ.CUSTOMER
        )


        self.customer_deposit = Deposit.objects.create(
            customer = self.customer,
            branch = self.branch,
            balance = 100 
        )

        self.admin_deposit = Deposit.objects.create(
            customer = self.admin_user,
            branch = self.branch,
            balance = 500 
        )

        self.another_customer_deposit = Deposit.objects.create(
            customer = self.another_customer,
            branch = self.branch,
            balance = 100 
        )

        self.loan_customer = Loan.objects.create(
            customer = self.customer,
            branch = self.branch,
            amount = 50
        )
        self.another_customer_loan = Loan.objects.create(
            customer = self.another_customer,
            branch = self.branch,
            amount = 100
        )
        self.admin_loan = Loan.objects.create(
            customer = self.admin_user,
            branch = self.branch,
            amount = 200
        )

        self.uri = '/api/loan/'
        return super().setUp()

    def test_api_anon_access(self):
        anon_client = test.APIClient()
        res = anon_client.get(self.uri)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) # Unauthorized

    def test_api_customer_access(self):
        customer_client = test.APIClient()
        customer_client.login(username=self.customer.username, password='test')
        res = customer_client.get(self.uri)
        self.assertTrue(status.is_success(res.status_code))

        data = LoanSerializer(self.loan_customer).data
        self.assertEqual(res.json(), [data])

        push_data = data.copy()
        uri = self.uri + str(push_data['id']) + '/'
        push_data.pop('id')
        push_data['amount'] = 5000
        res = customer_client.put(uri, data=push_data)
        self.assertTrue(status.is_client_error(res.status_code))

        res = customer_client.post(self.uri, data=push_data)
        self.assertTrue(status.is_client_error(res.status_code))

        res = customer_client.delete(uri)
        self.assertTrue(status.is_client_error(res.status_code))

    def test_api_admin_access(self):
        admin_client = test.APIClient()
        admin_client.login(username=self.admin_user.username, password='test')
        res = admin_client.get(self.uri)
        self.assertTrue(status.is_success(res.status_code))

        data = LoanSerializer(Loan.objects.all(), many=True).data
        self.assertEqual(res.json(), data)

        push_data = dict(data[0])
        push_data['amount'] = 5000
        uri = self.uri + str(push_data['id']) + '/'
        push_data.pop('id')
        res = admin_client.put(uri, data=push_data)
        self.assertTrue(status.is_success(res.status_code))

        res = admin_client.post(self.uri, data=push_data)
        self.assertTrue(status.is_success(res.status_code))

        res = admin_client.delete(uri)
        self.assertTrue(status.is_success(res.status_code))
