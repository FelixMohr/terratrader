from src import const


class Params(object):

    def __init__(self):
        self.amount_luna = 1.0
        self.amount_bluna = 1.0
        self.inv_sell_price = 0.985
        self.buy_price = 0.975
        self.mode = const.buy
        self.spread = 0.007
        self.sleep_time_seconds = 3
        self.sleep_time_loans_seconds = 5
        self.do_log = False
        self.never_log = False
        self.repay_ratio = 0.8

    def set_logging(self, mode: bool):
        self.do_log = mode

    def should_log(self):
        return self.do_log and not self.never_log

    def switch_mode(self):
        self.mode = abs(self.mode - 1)
