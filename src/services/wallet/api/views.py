from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from src.services.wallet.api.serializers import WalletSerializer, TransactionSerializer, BankSerializer, \
    BankAccountSerializer
from src.services.wallet.models import Wallet, Transaction, Bank, BankAccount


class WalletRetrieveAPIVIew(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


class TransactionListCreateAPIView(ListCreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankListAPIView(ListAPIView):
    queryset = Bank.objects.filter(is_active=True)
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]


class BankAccountListCreateAPIView(ListCreateAPIView):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
