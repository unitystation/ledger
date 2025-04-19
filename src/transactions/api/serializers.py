from rest_framework import serializers

from ..models import Movement


class MoneyMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'
        read_only_fields = ['balance_after']

    def create(self, validated_data):
        instance = Movement.objects.create(**validated_data)
        return instance
