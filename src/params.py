from src import const


class Params(object):

    def __init__(self):
        self.amount_luna = 1.0
        self.amount_bluna = 1.0
        self.inv_sell_price = 0.988
        self.buy_price = 0.982
        self.mode = const.buy
        self.spread = 0.007
        self.sleep_time_seconds = 3
