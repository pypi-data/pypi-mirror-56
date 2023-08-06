from blockapi.services import (
    BlockchainAPI
)


class BtcAPI(BlockchainAPI):
    """
    coins: bitcoin-cash
    API docs: https://bch.btc.com/api-doc#API
    Explorer: https://btc.com
    """

    active = True

    symbol = 'BCH'
    base_url = 'https://bch-chain.api.btc.com/v3'
    rate_limit = 0
    coef = 1e-8
    max_items_per_page = None
    page_offset_step = None
    confirmed_num = None

    supported_requests = {
        'get_balance': '/address/{address}',
    }

    def get_balance(self):
        response = self.request('get_balance',
                                address=self.address)
        if not response:
            retval = 0

        try:
            retval = response['data']['balance'] * self.coef
        except KeyError:
            retval = 0

        return [{'symbol': self.symbol, 'amount': retval}]
