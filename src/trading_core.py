from typing import Dict

from terra_sdk.client.lcd import LCDClient, Wallet
from terra_sdk.core import Coins
from terra_sdk.core.auth import StdFee, StdTx
from terra_sdk.core.broadcast import BlockTxBroadcastResult
from terra_sdk.core.wasm import MsgExecuteContract

from src import const
from src.helpers import to_uluna, get_buy_dict, get_sell_dict, info, start_halo, stop_halo
from src.params import Params


def get_bluna_for_luna_price(terra: LCDClient, params: Params):
    spinner = start_halo('Retrieving bluna for luna price', params)
    sent_amount = to_uluna(params.amount_luna)
    result = get_swap_price(sent_amount, terra, const.luna_info)
    stop_halo(spinner)
    return result


def get_luna_for_bluna_price(terra: LCDClient, params: Params):
    spinner = start_halo('Retrieving bluna for luna price', params)
    sent_amount = to_uluna(params.amount_bluna)
    result = get_swap_price(sent_amount, terra, const.bluna_info)
    stop_halo(spinner)
    return result


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
    msg = MsgExecuteContract(wallet.key.acc_address, const.bluna_contract,
                             get_sell_dict(belief_price, params))
    return execute_contract(msg, terra, wallet, params)


def execute_contract(exec, terra, wallet, params: Params) -> bool:
    execute_tx: StdTx = wallet.create_and_sign_tx(msgs=[exec])
    execute_tx_result: BlockTxBroadcastResult = terra.tx.broadcast(execute_tx)
    info("transaction hash:", params.should_log())
    info(str(execute_tx_result.txhash), params.should_log())
    return execute_tx_result.code is None
