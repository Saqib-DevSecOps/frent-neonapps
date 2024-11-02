class BalanceDLL:
    def __init__(self, available_balance, available_balance_currency, pending_balance, pending_balance_currency):
        self.available_balance = available_balance
        self.available_balance_currency = available_balance_currency
        self.pending_balance = pending_balance
        self.pending_balance_currency = pending_balance_currency


# TESTED - REQUIRED - CONNECT
class ExternalAccountDLL:

    def __init__(self, data):
        self.id = data.get('id')
        self.object = data.get('object')
        self.country = data.get('country')
        self.fingerprint = data.get('fingerprint')
        self.account = data.get('account')
        self.last4 = data.get('last4')
        self.meta_data = data.get('metadata')
        self.full_json = data

        if self.object == 'card':

            self.name = data.get('name')
            self.tokenization_method = data.get('tokenization_method')
            self.wallet = data.get('wallet')
            self.brand = data.get('brand')
            self.exp_month = data.get('exp_month')
            self.exp_year = data.get('exp_year')
            self.cvc_check = data.get('cvc_check')
            self.funding = data.get('funding')
            self.dynamic_last4 = data.get('dynamic_last4')
            self.address_city = data.get('address_city')
            self.address_country = data.get('address_country')
            self.address_line1 = data.get('address_line1')
            self.address_line1_check = data.get('address_line1_check')
            self.address_line2 = data.get('address_line2')
            self.address_state = data.get('address_state')
            self.address_zip = data.get('address_zip')
            self.address_zip_check = data.get('address_zip_check')

        elif self.object == 'bank_account':

            self.account_holder_name = data.get('account_holder_name')
            self.account_holder_type = data.get('account_holder_type')
            self.bank_name = data.get('bank_name')
            self.currency = data.get('currency')
            self.routing_number = data.get('routing_number')
            self.status = data.get('status')

        else:
            raise ValueError(f"Unsupported account object type: {self.object}")

    def __str__(self):
        if self.object == 'card':
            return f"{self.brand} ending in {self.last4}"
        elif self.object == 'bank_account':
            return f"Bank account ending in {self.last4}"
        else:
            return f"Unsupported account object type: {self.object}"

    def get_id(self):
        return self.id

    def is_card(self):
        return self.object == 'card'

