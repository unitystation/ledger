from rest_framework import serializers

from .calc import recalculate_balances
from ..models import Movement


class MoneyMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = ['id', 'type', 'amount_usd', 'created_at', 'balance_after']
        read_only_fields = ['balance_after']

    def create(self, validated_data):
        instance = Movement.objects.create(**validated_data)
        recalculate_balances()
        return instance
