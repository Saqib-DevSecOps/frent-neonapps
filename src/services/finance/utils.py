from src.services.finance.models import Transaction


def withdrawal_balance_calculation(withdrawal):
    if withdrawal.status == 'accepted':
        transaction = Transaction(
            user=withdrawal.user,
            amount=withdrawal.amount,
            transaction_type='withdrawal',
            description=f'Withdrawal of {withdrawal.amount} completed successfully'
        )
        transaction.save()
