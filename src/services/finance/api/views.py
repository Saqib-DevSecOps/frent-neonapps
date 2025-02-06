from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from src.services.finance.api.serializers import WalletSerializer, BankAccountSerializer, WithdrawalSerializer, \
    TransactionSerializer, ChargeSerializer
from src.services.finance.models import Wallet, BankAccount, Withdrawal, Transaction, Charge


class WalletRetrieveAPIVIew(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


class BankAccountListCreateView(ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankAccountDeleteAPIView(RetrieveAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(BankAccount, user=self.request.user, pk=self.kwargs['pk'])


class WithdrawalListCreateAPIView(ListCreateAPIView):
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionListAPIView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class ChargeListAPIView(ListAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated]
