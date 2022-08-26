from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, UserManager


# class MyUserManager(UserManager):
#     def create_superuser(self, email, date_of_birth, password=None):
#         """
#         Creates and saves a superuser with the given national number and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


class User(AbstractUser):
    class Typ(models.IntegerChoices):
        CUSTOMER = 0, _('Customer')
        STAFF = 1, _('Staff')
        SUPERUSER = 2, _('Super User')

    national_no = models.CharField(verbose_name="National number", max_length=10,
        validators=[
            RegexValidator(
                regex='^[1-9][0-9]{9}$',
                message='National number must be numeric and 10 digits',
                code='invalid_national_number'
            ),], unique=True ,null=False, blank=False)
    username = models.CharField(max_length=100,
        validators=[
            RegexValidator(
                regex='^[A-Za-z0-9_]+$',
                message='Username must be only letters, numbers, and underscore.',
                code='invalid_username'
            ),
        ], unique=True ,null=False, blank=False
    )
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    typ = models.IntegerField(choices=Typ.choices, null=False,blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self) -> str:
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *arg, **kwargs) -> None:
        if self.typ == 0:
            self.is_staff = False
            self.is_superuser = False
        elif self.typ == 1:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = True
            self.is_superuser = True
        return super().save(*arg, **kwargs)
    