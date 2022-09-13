from rest_framework import test, status
from django.test import TestCase
from branch.models import Branch
from django.contrib.auth import get_user_model
from branch.api.serializers import BranchSerializer

class TestBranchAPI(TestCase):
    def setUp(self) -> None:
        self.customer = get_user_model().objects.create(
            national_no='1234567890',
            username='customer',
            first_name='test',
            last_name='test',
            address='test...',
            email='',
            typ=0,
        )
        self.customer.set_password('test')
        self.customer.save()

        self.admin_user = get_user_model().objects.create(
            national_no='9876543210',
            username='admin',
            first_name='test',
            last_name='test',
            address='test...',
            email='',
            typ=1,
        )
        self.admin_user.set_password('test')
        self.admin_user.save()

        self.branch = Branch.objects.create(name='test', city='Test', address='test...')

        self.uri = '/api/branch/'
        return super().setUp()

    def test_api_anonymous(self) -> None:
        anon_client = test.APIClient()
        res = anon_client.get(self.uri)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) # Unauthorized
        
    def test_api_unauthorized(self) -> None:
        auth_client = test.APIClient()
        auth_client.login(username='customer', password='test')
        res = auth_client.get(self.uri)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN) # Forbidden

    def test_api_admin(self) -> None:
        auth_client = test.APIClient()
        auth_client.login(username='admin', password='test')

        res = auth_client.get(self.uri)

        self.assertEqual(res.status_code, status.HTTP_200_OK) # OK

        branches = BranchSerializer(Branch.objects.all(), many=True).data
        self.assertEqual(branches, res.json()) # check for data it will access
        
        uri = self.uri + str(self.branch.id) + '/'
        res = auth_client.get(uri)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = {'name':'test', 'city':'Tehran', 'address':'test...'}
        res = auth_client.put(uri, data, format='json')
        data['id'] = self.branch.id
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), data)

        data = {'name': 'new', 'city':'test'}
        res = auth_client.post(self.uri, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        res = auth_client.delete(uri)
        self.assertTrue(status.is_success(res.status_code))


