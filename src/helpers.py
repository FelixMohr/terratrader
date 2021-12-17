from typing import List, Dict, Union

import datetime
import terra_sdk.client.lcd
from halo import Halo
from terra_sdk.core import Coins

from src import const
from src.params import Params
from terra_sdk.client.lcd import LCDClient, Wallet
from terra_sdk.key.raw import RawKey
import os
import base64
import time
import requests


def create_params() -> Params:
    return Params()


def create_terra() -> LCDClient:
    prices = requests.get(const.gas_price_url).json()
    uusd = prices["uusd"]
    coins = Coins(uusd=uusd)
    client = LCDClient(chain_id=const.chain_id, url=const.lcd_url, gas_prices=coins, gas_adjustment=1.4)
    info("Connected to " + const.chain_id + " via " + const.lcd_url)
    return client


def create_wallet(client: LCDClient) -> Wallet:
    pk = get_pk().strip()
    key = RawKey.from_hex(pk)
    wallet = terra_sdk.client.lcd.Wallet(client, key)
    return wallet


def get_arg_safe(args: List[str], idx=0) -> str:
    if not len(args):
        warn("not enough arguments")
        return ""
    return args[idx]


def to_uluna(luna: float) -> int:
    return round(luna * 1000000)


def from_uluna(uluna: int) -> float:
    return uluna / 1000000.0


def get_sell_msg(max_spread: float, belief_price: float) -> str:
    jsn = '{"swap":{"max_spread":"' + str(max_spread) + '","belief_price":"' + str(belief_price) + '"}}'
    encoded = jsn.encode()
    return str(base64.b64encode(encoded), "utf-8")


def get_sell_dict(belief_price: float, params: Params) -> Dict:
    msg = get_sell_msg(params.spread, belief_price)
    amount = str(to_uluna(params.amount_bluna))
    return {
        "send": {
            "amount": amount,
            "contract": const.luna_bluna,
            "msg": msg
        }
    }


def get_buy_dict(belief_price: float, params: Params) -> Dict:
    amount = str(to_uluna(params.amount_luna))
    return {
        "swap": {
            "belief_price": str(belief_price),
            "max_spread": str(params.spread),
            "offer_asset": {
                "amount": amount,
                "info": {
                    "native_token": {
                        "denom": "uluna"
                    }
                }
            }
        }
    }


def get_pk() -> str:
    return os.getenv('PK')


def info(s: str, do_log=False):
    print(" 🛰    {}".format(s))
    if do_log:
        with open(const.log_file, 'a+') as f:
            s = str(datetime.datetime.now()) + " -- " + s + "\n"
            f.write(s)


def warn(s: str):
    print(" 👾    {}".format(s))


def get_system_time_millis() -> int:
    return round(time.time() * 1000)


def start_halo(text: str, params: Params, spinner='dots', text_color='magenta') -> Union[Halo | None]:
    if not params.never_log:
        spinner = Halo(text=text, spinner=spinner, text_color=text_color)
        spinner.start()
        return spinner


def stop_halo(spinner: Union[Halo | None]):
    if spinner:
        spinner.stop()
