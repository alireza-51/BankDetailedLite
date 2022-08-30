from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'national_no',
            'username',
            'first_name',
            'last_name',
            'address',
            'email',
            'password',
            'typ',

        ]
        read_only_fields = ('id', 'typ')
        extra_kwargs = {
            'password': {'write_only': True}
        }



    def create(self, validated_data):
        user = User.objects.create(
            national_no=validated_data['national_no'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            address=validated_data['address'],
            email=validated_data['email'],
            typ=0,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user