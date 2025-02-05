from rest_framework import serializers

from src.apps.stripe.models import Transfer, Payout


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ["id", "amount", "currency", "description", "destination", "source_type", 'created']


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ["id", "amount", "type", "currency", "status", "description", "source_type", "arrival_date", "created"]
