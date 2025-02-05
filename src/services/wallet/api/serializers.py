# from rest_framework import serializers
#
# from src.services.wallet.models import Wallet, Transaction, Bank, BankAccount
#
#
# class WalletSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wallet
#         fields = ["id", "user", "total_amounts", "total_deposits", "total_earnings", "total_withdrawals",
#                   "balance_available", "balance_pending", "outstanding_charges"]
#
#
# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ["id", "amount", "fee", "description", "transaction_type", 'status', 'payment_type', 'created_at',
#                   'updated_at']
#         read_only_fields = ['status', 'created_at', 'updated_at']
#
#
# class BankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bank
#         fields = ['id', 'name', 'is_active', 'created_at']
#
#
# class BankAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankAccount
#         fields = [
#             'id', 'user', 'account_holder_name', 'account_number',
#             'account_iban', 'account_type', 'account_currency',
#             'swift_code', 'routing_number', 'bank', 'country',
#             'bank_city', 'bank_address', 'bank_postal_code',
#             'is_active', 'created_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'user']
