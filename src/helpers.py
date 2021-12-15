import terra_sdk.client.lcd
from src import const
from src.params import Params
from terra_sdk.client.lcd import LCDClient, Wallet
from terra_sdk.key.raw import RawKey
import os


def create_params() -> Params:
    return Params("")


def create_terra() -> LCDClient:
    client = LCDClient(chain_id=const.chain_id, url=const.lcd_url)
    info("Connected to " + const.chain_id + " via " + const.lcd_url)
    return client


def create_wallet(client: LCDClient) -> Wallet:
    pk = get_pk().strip()
    key = RawKey.from_hex(pk)
    wallet = terra_sdk.client.lcd.Wallet(client, key)
    return wallet


def get_pk() -> str:
    return os.getenv('PK')


def info(s: str):
    print(" 🛰    {}".format(s))
