from terra_sdk.client.lcd import Wallet
from terra_sdk.core import Coins, Coin
from terra_sdk.core.wasm import MsgExecuteContract

from src import const
from src.helpers import info, to_u_unit, get_infos_from_url, from_u_unit, warn
from src.messages import get_borrower_info_msg, get_borrow_limit_uust_from_msg, get_loan_uust_from_msg, \
    get_borrow_limit_msg, get_withdraw_msg, get_repay_stable_msg
from src.params import Params


def get_loan_uust(wallet: Wallet):
    terra = wallet.lcd
    result = terra.wasm.contract_query(const.market_address, get_borrower_info_msg(wallet.key.acc_address))
    return get_loan_uust_from_msg(result)


def get_borrow_limit_uust(wallet: Wallet):
    terra = wallet.lcd
    result = terra.wasm.contract_query(const.overseer_address, get_borrow_limit_msg(wallet.key.acc_address))
    return get_borrow_limit_uust_from_msg(result)


def withdraw(wallet: Wallet, amount_aust: float, params: Params):
    msg = MsgExecuteContract(wallet.key.acc_address, const.aust_address,
                             get_withdraw_msg(amount_aust))
    return execute_contract(msg, wallet, params)


def execute_contract(exc, wallet, params: Params) -> bool:
    execute_tx = wallet.create_and_sign_tx(msgs=[exc])
    execute_tx_result = wallet.lcd.tx.broadcast(execute_tx)
    info(str(execute_tx_result), params.should_log())
    return True


def get_aust_to_ust_rate() -> float:
    rate_str = get_infos_from_url(const.market_api_url, ["exchange_rate"])[0]
    if not rate_str:
        raise ValueError("could not get exchange rate from {}".format(const.market_api_url))
    return float(rate_str)


def execute_repay(wallet: Wallet, params: Params, current_loan_uust: int):
    # repays 1/3 of the current loan
    if current_loan_uust <= 0:
        warn("currently no loan, skipping")
        return

    try:
        rate = get_aust_to_ust_rate()
    except ValueError:
        warn("not able to fetch aUST value, using 1.155")
        rate = 1.155
    current_loan_ust = from_u_unit(current_loan_uust)
    repay_ust = current_loan_ust / 3
    safe_balance_ust = from_u_unit(get_safe_balance(wallet))

    if safe_balance_ust < repay_ust:
        withdraw_aust_amount = current_loan_ust / (3 * rate) - safe_balance_ust
        withdraw(wallet, withdraw_aust_amount, params)
        safe_balance_ust = from_u_unit(get_safe_balance(wallet))

    info("repaying {}, safe balance is {}".format(repay_ust, safe_balance_ust))
    repay(wallet, repay_ust, params)


def repay(wallet: Wallet, amount_ust: float, params: Params):
    msg = MsgExecuteContract(wallet.key.acc_address, const.market_address,
                             get_repay_stable_msg(), Coins(uusd=to_u_unit(amount_ust)))
    info("executing msg:")
    info(str(msg))
    return execute_contract(msg, wallet, params)


def get_balance(wallet: Wallet):
    coin: Coin | None = wallet.lcd.bank.balance(wallet.key.acc_address).get('uusd')
    if coin:
        return coin.amount
    return 0


def get_safe_balance(wallet: Wallet) -> int:
    # returns the balance minus 1 UST for future transactions
    return max(get_balance(wallet) - 1000000, 0)
