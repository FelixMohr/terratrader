from time import sleep

from terra_sdk.client.lcd import LCDClient, Wallet

from src.trading_core import get_bluna_for_luna_price, buy, get_luna_for_bluna_price, sell
from src.loans_core import get_loan_uust, get_borrow_limit_uust, execute_repay
from src.params import Params
from src.helpers import info, get_system_time_millis, warn
from src import const


def run(params: Params, terra: LCDClient, wallet: Wallet):
    info("starting bot. send keyboard interrupt to stop")
    params.set_logging(True)
    last_timestamp = get_system_time_millis()
    last_timestamp_loans = get_system_time_millis()
    while True:
        seconds_passed_trade = (get_system_time_millis() - last_timestamp) / 1000.0
        seconds_passed_loans = (get_system_time_millis() - last_timestamp_loans) / 1000.0
        try:
            if seconds_passed_loans >= params.sleep_time_loans_seconds:
                check_loans(params, wallet)
                last_timestamp_loans = get_system_time_millis()
            check_trades(params, terra, wallet)
            sleep(max(0, params.sleep_time_seconds - seconds_passed_trade))
            last_timestamp = get_system_time_millis()
        except KeyboardInterrupt:
            break
    params.set_logging(False)
    print()
    info("bot was stopped.")


def check_trades(params, terra, wallet):
    if params.mode == const.buy:
        check_buy(params, terra, wallet)
    else:
        check_sell(params, terra, wallet)


def check_buy(params: Params, terra: LCDClient, wallet: Wallet):
    return_amount, price = get_bluna_for_luna_price(terra, params)
    if price > params.buy_price:
        info("price {} vs. {}, not buying".format(price, params.buy_price), params.should_log())
        if price - params.buy_price <= 0.001:
            params.sleep_time_seconds = 1
        else:
            params.sleep_time_seconds = 3
    else:
        result = buy(params, terra, price, wallet)
        if result:
            info("🚀 bought bLuna for {} luna".format(params.amount_luna), params.should_log())
            params.switch_mode()
        else:
            warn("error while executing transaction")


def check_sell(params: Params, terra: LCDClient, wallet: Wallet):
    return_amount, price = get_luna_for_bluna_price(terra, params)
    diff = 1 / price - params.inv_sell_price
    if diff < 0:
        info("price {} vs. {}, not selling".format(1 / price, params.inv_sell_price), params.should_log())
        if abs(diff) <= 0.001:
            params.sleep_time_seconds = 1
        else:
            params.sleep_time_seconds = 3
    else:
        result = sell(params, terra, price, wallet)
        if result:
            info("🚀 sold {} bLuna".format(params.amount_bluna), params.should_log())
            params.switch_mode()
        else:
            warn("error while executing transaction")


def check_loans(params, wallet):
    loan = get_loan_uust(wallet)
    borrow_limit = get_borrow_limit_uust(wallet)
    used = loan / borrow_limit
    if used >= params.repay_ratio:
        info("used ratio is {}, repaying loan partially.".format(used))
        execute_repay(wallet, params, loan)
    else:
        info("used ratio is {} of {}.".format(used, params.repay_ratio))
