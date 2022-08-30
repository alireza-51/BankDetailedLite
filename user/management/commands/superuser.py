from getpass import getpass
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.contrib.auth import get_user_model



class Command(BaseCommand):
    help = 'Creates super user by given fields.'

    def handle(self, *args, **options):
        nn = input('National Number: ')
        username = input('Username: ')
        fn = input('First name: ')
        ln = input('Last name: ')
        email = input('Email: ')
        User = get_user_model()
        try:
            superuser = User.objects.get(Q(national_no=nn) | Q(username=username))
            if superuser:
                raise CommandError('User with this national number or username exists.')
        except User.DoesNotExist:
            superuser = User.objects.create(
                national_no=nn,
                username=username,
                first_name=fn,
                last_name=ln,
                email=email,
                typ=2
            )
            password = None
            while password == None:
                password = getpass('password: ')
                password2 = getpass('password (again): ')
                print('password : {}'.format(password))
                if password != password2:
                    self.stderr.write("Error: Password didn't match")
                    password = None
                    continue
            superuser.set_password(password)
            superuser.save()
            self.stdout.write(self.style.SUCCESS('Super User created.'))
            