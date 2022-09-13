from django.test import TestCase
from branch.models import Branch


class TestBranch(TestCase):
    def setUp(self) -> None:
        self.branch = Branch.objects.create(name='test', city='Tehran', address = 'test...')

    def test_branch(self):
        self.assertEqual(self.branch.name, 'test')
        self.assertEqual(self.branch.city, 'Tehran')
        self.assertEqual(self.branch.address, 'test...')
