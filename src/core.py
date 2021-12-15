from typing import Dict

from terra_sdk.client.lcd import LCDClient
from src import const
from src.helpers import to_uluna
from src.params import Params


def get_bluna_for_luna_price(terra: LCDClient, params: Params):
    sent_amount = to_uluna(params.amount_luna)
    return get_swap_price(sent_amount, terra, const.luna_info)


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
    return return_amount, sent_amount/return_amount


def buy(params: Params, terra: LCDClient, belief_price: float):
    pass


def sell(params: Params, terra: LCDClient, belief_price: float):
    pass
