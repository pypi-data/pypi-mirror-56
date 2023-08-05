from . import PriceType
from .Money import Money


class Price(dict):
    """
    {
      "type": enum(PriceType),
      "amount": {
        object(Money)
      },
    }
    """

    def __init__(self, price_type: PriceType, amount: Money):
        super().__init__()

        self['amount'] = amount
        self['priceType'] = price_type
