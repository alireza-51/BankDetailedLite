from dataclasses import field
from rest_framework import serializers
from deposit.models import Deposit, Withdrawal


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('account_no',)