from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from src.apps.stripe.bll import stripe_transfer_to_connect_account
from src.services.finance.models import Wallet, BankAccount, Withdrawal, Transaction, Charge


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "user", "total_amounts", "total_deposits", "total_earnings", "total_withdrawals",
                  "balance_available", "balance_pending", "outstanding_charges", "connect_pending_balance",
                  "connect_available_balance", "connect_available_balance_currency", "connect_pending_balance_currency"
                  ]


class BankAccountSerializer(serializers.ModelSerializer):
    last_4_digits = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = [
            'id', 'user', 'account_holder_name', 'description', 'status',
            'is_active', 'account_type', 'bank_name', 'iban',
            'currency', 'created_at', 'updated_at', 'last_4_digits'
        ]
        read_only_fields = ['status', 'is_active', 'created_at', 'updated_at', 'last_4_digits']

    def get_last_4_digits(self, obj):
        return obj.last_4_digits()

    def create(self, validated_data):
        return BankAccount.objects.create(**validated_data)


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['id', 'amount', 'withdrawal_type', 'status', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_amount(self, value):
        """Ensure the amount is a valid positive integer."""
        if value <= 0:
            raise serializers.ValidationError('Amount must be a positive number.')
        return value

    def validate(self, data):
        """Custom validation for the overall withdrawal request."""
        # get user from request
        user = self.context['request'].user
        amount = data.get('amount')
        withdrawal_type = data.get('withdrawal_type')
        status = data.get('status')

        # Ensure user is provided
        if not user:
            raise serializers.ValidationError({'user': 'User is required for withdrawal.'})

        wallet = user.get_user_wallet()

        # Ensure the user is a vendor
        # Ensure sufficient balance in the wallet
        if amount > wallet.balance_available:
            raise serializers.ValidationError({'amount': 'Insufficient balance in wallet.'})

        # Withdrawal type validation
        if withdrawal_type == 'bank':
            if not user.bank_account_active():
                raise serializers.ValidationError({'withdrawal_type': 'User does not have an active bank account.'})
        elif withdrawal_type == 'connect':
            if not user.is_stripe_account_active():
                raise serializers.ValidationError({'withdrawal_type': 'User connect account is not active.'})
        else:
            raise serializers.ValidationError({'withdrawal_type': 'Invalid withdrawal type.'})

        # Handle first-time status (must be pending)
        if not self.instance:  # This is a new withdrawal
            previous_withdrawals = Withdrawal.objects.filter(user=user, status='pending').exists()
            if previous_withdrawals:
                raise serializers.ValidationError({'status': 'Your previous withdrawal request is still pending.'})

            if status != 'pending':
                raise serializers.ValidationError({'status': 'Status must be pending at the start.'})

        # If the withdrawal is not new, ensure it is not in an invalid state (accepted/cancelled)
        if self.instance:
            previous_status = self.instance.status
            if previous_status in ['accepted', 'cancelled']:
                raise serializers.ValidationError({'status': 'Cancelled or accepted requests cannot be updated.'})

        # If withdrawal type is 'connect' and status is 'accepted', perform the Stripe transfer
        if withdrawal_type == 'connect' and status == 'accepted':
            success, obj = self.handle_connect_withdrawal(user, amount)
            if not success:
                raise serializers.ValidationError({'status': obj})
        return data

    def handle_connect_withdrawal(self, user, amount):
        """Handles withdrawal to Stripe Connect account."""
        success = False
        try:
            amount = int(amount)
        except ValueError:
            raise serializers.ValidationError("Please enter a valid integer amount.")

        # Call your method for the Stripe transfer (this should return success and any relevant info)
        success, obj = stripe_transfer_to_connect_account(user=user, amount=amount)
        return success, obj


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        # AMOUNT CHECK
        if data['amount'] <= 0:
            raise ValidationError('Amount must be greater than 0')

        # USER MUST HAVE WALLET
        wallet = Wallet.objects.filter(user=user)
        if not wallet.exists():
            raise ValidationError('User must have wallet to perform transaction')
        wallet = wallet.first()

        # WALLET MUST HAVE GREATER AMOUNT OF MONEY THAN
        if data['transaction_type'] in ['withdrawal', 'charge']:
            if wallet.balance_available < data['amount']:
                raise ValidationError('Insufficient balance to perform this transaction')

        # IF ALREADY EXISTS THEN DON'T ALLOW TO CHANGE STATUS
        if self.instance and self.instance.pk:  # Check if it's an update operation
            previous_status = Transaction.objects.get(pk=self.instance.pk).status
            if previous_status:
                raise ValidationError("You aren't allowed to change status of transaction")

        return data


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ['id', 'fee_amount', 'fee_type', 'currency', 'description', 'status', 'is_active', 'created_at',
                  'updated_at']

    def validate(self, data):
        # AMOUNT CHECK
        if data['fee_amount'] <= 0:
            raise ValidationError('Fee amount must be greater than 0')

        # IF PREVIOUS STATUS IS COMPLETED DON'T ALLOW TO CHANGE
        if self.instance and self.instance.pk:  # Check if it's an update operation
            previous_status = Charge.objects.get(pk=self.instance.pk).status

            if previous_status == data['status']:
                raise ValidationError('Cannot change status to same status')

            if previous_status == 'completed':
                raise ValidationError('Cannot change status of completed charge')

        # IF STATUS IS COMPLETED
        if data['status'] == 'completed':
            wallet = self.context['request'].user.get_user_wallet()  # Assuming `user` is in the request context
            available_balance = wallet.balance_available

            if available_balance < data['fee_amount']:
                raise ValidationError('Insufficient balance')

        return data
