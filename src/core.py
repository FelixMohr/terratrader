from typing import Dict

from halo import Halo
from terra_sdk.client.lcd import LCDClient, Wallet
from terra_sdk.core import Coins
from terra_sdk.core.wasm import MsgExecuteContract

from src import const
from src.helpers import to_uluna, get_buy_dict, get_sell_dict, info
from src.params import Params


@Halo(text='Retrieving bluna for luna price', spinner='dots', text_color='magenta')
def get_bluna_for_luna_price(terra: LCDClient, params: Params):
    sent_amount = to_uluna(params.amount_luna)
    return get_swap_price(sent_amount, terra, const.luna_info)


@Halo(text='Retrieving luna for bluna price', spinner='dots', text_color='magenta')
def get_luna_for_bluna_price(terra: LCDClient, params: Params):
    sent_amount = to_uluna(params.amount_bluna)
    return get_swap_price(sent_amount, terra, const.bluna_info)


def get_swap_price(sent_amount: int, terra: LCDClient, info_dict: Dict):
    return_amount = int(terra.wasm.contract_query(const.luna_bluna, {
        "simulation": {
            "offer_asset": {
                "info": info_dict,
                "amount": str(sent_amount)
            }}
    })['return_amount'])
    return return_amount, sent_amount / return_amount


def buy(params: Params, terra: LCDClient, belief_price: float, wallet: Wallet) -> bool:
    msg = MsgExecuteContract(wallet.key.acc_address, const.luna_bluna,
                             get_buy_dict(belief_price, params), Coins(uluna=to_uluna(params.amount_luna)))
    return execute_contract(msg, terra, wallet, params)


def sell(params: Params, terra: LCDClient, belief_price: float, wallet: Wallet) -> bool:
    msg = MsgExecuteContract(wallet.key.acc_address, const.luna_bluna,
                             get_sell_dict(belief_price, params))
    return execute_contract(msg, terra, wallet, params)


def execute_contract(exec, terra, wallet, params: Params) -> bool:
    execute_tx = wallet.create_and_sign_tx(msgs=[exec])
    execute_tx_result = terra.tx.broadcast(execute_tx)
    info(str(execute_tx_result), params.do_log)
    return True
