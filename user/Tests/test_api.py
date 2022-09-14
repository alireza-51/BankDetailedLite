from django.test import TestCase
from rest_framework import test, status
from django.contrib.auth import get_user_model
from user.api.serializers import UserSerializer

User = get_user_model()

class TestUserAPI(TestCase):
    def setUp(self) -> None:
        self.customer_user = User(
            national_no = '1234567890',
            username = 'customer',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        self.customer_user.set_password('test')
        self.customer_user.save()

        self.another_customer = User(
            national_no = '5469871230',
            username = 'another_customer',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        self.another_customer.save()

        self.admin_user = User(
            national_no = '9876543210',
            username = 'admin',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.STAFF
        )
        self.admin_user.set_password('test')
        self.admin_user.save()

        self.uri = '/api/user/'
        return super().setUp()

    def test_anon(self):
        anon_client = test.APIClient()
        res = anon_client.get(self.uri)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {
            'username': 'anon_user',
            'national_no': '5469873210',
            'first_name': 'test',
            'last_name': 'test',
            'address': 'test...',
            'typ': 0,
            'password': 'test'
        }
        res = anon_client.post(self.uri, data)
        self.assertTrue(status.is_success(res.status_code))

    def test_customer(self):
        customer_client = test.APIClient()
        customer_client.login(username='customer', password='test')

        res = customer_client.get(self.uri)
        self.assertTrue(status.is_success(res.status_code))

        customer_data = UserSerializer(self.customer_user).data
        self.assertEqual(res.json(), [customer_data])

        uri = self.uri + str(customer_data.get('id', self.customer_user.id)) + '/'
        customer_data['email'] = 'test@test.test'
        customer_data['address'] = 'test...'
        customer_data['password'] = 'test'
        res = customer_client.put(uri, customer_data)
        self.assertTrue(status.is_success(res.status_code))

        admin_uri = self.uri + str(self.admin_user.id) + '/'
        res = customer_client.put(admin_uri, customer_data)
        self.assertTrue(status.is_client_error(res.status_code))

        customer_client.force_authenticate(user=self.customer_user)
        res = customer_client.delete(uri)
        self.assertTrue(status.is_success(res.status_code))
        self.customer_user.save()
    
    def test_admin(self):
        admin_client = test.APIClient()
        admin_client.login(username='admin', password='test')

        res = admin_client.get(self.uri)
        self.assertTrue(status.is_success(res.status_code))

        data = UserSerializer(User.objects.all(), many=True).data
        self.assertEqual(res.json(), data)

        uri = self.uri + str(self.another_customer.id) + '/'
        data = UserSerializer(self.another_customer).data
        data['email'] = 'test_another@test.com'
        data['address'] = 'test...'
        data['password'] = 'test'
        res = admin_client.put(uri, data) 
        self.assertTrue(status.is_success(res.status_code))

        res = admin_client.delete(uri)
        self.assertTrue(status.is_success(res.status_code))
        self.another_customer.save()
    
    def test_token_access(self):
        uri_token = '/api/login/token/'
        uri_refresh = '/api/login/token/refresh/'

        token_client = test.APIClient()
        data = {
            'username':'admin',
            'password':'test'
        }
        res = token_client.post(uri_token, data)
        self.assertTrue(status.is_success(res.status_code))
        
        token_data = res.json()
        res = token_client.post(uri_refresh, {'refresh':token_data['refresh']})
        self.assertTrue(status.is_success(res.status_code))
