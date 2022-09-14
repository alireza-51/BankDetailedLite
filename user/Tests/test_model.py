from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class TestUser(TestCase):
    def setUp(self) -> None:
        self.customer = User.objects.create(
            national_no = '9876543210',
            username = 'customer',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        self.staff = User.objects.create(
            national_no = '1234567890',
            username = 'staff',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.STAFF
        )
        self.super_user = User.objects.create(
            national_no = '1237894560',
            username = 'superuser',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.SUPERUSER
        )
        return super().setUp()
    
    def test_typ(self):
        self.assertTrue(self.super_user.is_superuser)
        self.assertTrue(self.staff.is_staff)
        self.assertFalse(self.customer.is_superuser)
        self.assertFalse(self.customer.is_staff)

    def test_national_number_re(self):
        user = User(
            national_no = '123',
            username = 'national_number_test',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        user = User(
            national_no = '123456789123',
            username = 'national_number_test',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

        user = User(
            national_no = '123456asdf',
            username = 'national_number_test',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

        user = User(
            national_no = '0123456789',
            username = 'national_number_test',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
        
        user = User(
            national_no = '4569873210',
            username = 'n!',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

        user = User(
            national_no = '1236598740',
            username = 'nat@',
            first_name = 'test',
            last_name = 'test',
            typ = User.Typ.CUSTOMER
        )
        with self.assertRaises(ValidationError):
            user.full_clean()