from time import sleep

from terra_sdk.client.lcd import LCDClient

from src.core import get_bluna_for_luna_price, buy, get_luna_for_bluna_price, sell
from src.params import Params
from src.helpers import info
from src import const


def run(params: Params, terra: LCDClient):
    info("starting bot. send keyboard interrupt to stop")
    while True:
        try:
            sleep(params.sleep_time_seconds)
            if params.mode == const.buy:
                check_buy(params, terra)
            else:
                check_sell(params, terra)
        except KeyboardInterrupt:
            break
    print()
    info("bot was stopped.")


def check_buy(params: Params, terra: LCDClient):
    return_amount, price = get_bluna_for_luna_price(terra, params)
    if price > params.buy_price:
        info("price {} > {}, not buying".format(price, params.buy_price))
        if price - params.buy_price <= 0.001:
            params.sleep_time_seconds = 1
        else:
            params.sleep_time_seconds = 3
    else:
        buy(params, terra)


def check_sell(params: Params, terra: LCDClient):
    return_amount, price = get_luna_for_bluna_price(terra, params)
    diff = 1 / price - params.inv_sell_price
    if diff < 0:
        info("price {} < {}, not selling".format(1 / price, params.inv_sell_price))
        if abs(diff) <= 0.001:
            params.sleep_time_seconds = 1
        else:
            params.sleep_time_seconds = 3
    else:
        sell(params, terra)
