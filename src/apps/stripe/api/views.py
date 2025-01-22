from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from stripe import AuthenticationError

from src.apps.stripe.bll import stripe_connect_account_create, stripe_connect_account_link


class ConnectWalletCreateAPIView(GenericAPIView):
    """
    Create a new Wallet for the User
    """
    serializer_class = None

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_stripe_connected():
            return Response({'detail': 'You have already connected your wallet'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            error, account = stripe_connect_account_create(user)
            if error:
                return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationError as e:
            return Response({'detail': f'Authentication error: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Your wallet has been connected successfully'},
                        status=status.HTTP_200_OK)


class ConnectWalletActivateAPIView(GenericAPIView):
    """
    Visit the Wallet Dashboard
    """

    def get_serializer_class(self):
        return None

    def get(self, request, *args, **kwargs):
        user = request.user
        wallet = user.get_user_wallet()
        try:
            error, url = stripe_connect_account_link(wallet.stripe_account_id)
            if error:
                return Response({'detail': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationError as e:
            return Response({'detail': f'Authentication error: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'url': url}, status=status.HTTP_200_OK)
