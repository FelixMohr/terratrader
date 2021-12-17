import base64
from typing import Dict

from src import const
from src.helpers import to_u_unit
from src.params import Params


def get_borrower_info_msg(borrower_address: str) -> Dict:
    return {
        "borrower_info": {"borrower": borrower_address}
    }


def get_loan_uust_from_msg(msg: Dict) -> int:
    return int(msg['loan_amount'])


def get_borrow_limit_msg(borrower_address: str) -> Dict:
    return {
        "borrow_limit": {"borrower": borrower_address}
    }


def get_borrow_limit_uust_from_msg(msg: Dict) -> int:
    return int(msg['borrow_limit'])


def get_repay_stable_msg() -> Dict:
    return {
        "repay_stable": {}
    }


def get_withdraw_msg(amount_aust: float) -> Dict:
    return {
        "send": {
            "amount": str(to_u_unit(amount_aust)),
            "contract": const.market_address,
            "msg": "eyJyZWRlZW1fc3RhYmxlIjp7fX0="
        }
    }


def get_sell_msg(max_spread: float, belief_price: float) -> str:
    jsn = '{"swap":{"max_spread":"' + str(max_spread) + '","belief_price":"' + str(belief_price) + '"}}'
    encoded = jsn.encode()
    return str(base64.b64encode(encoded), "utf-8")


def get_sell_dict(belief_price: float, params: Params) -> Dict:
    msg = get_sell_msg(params.spread, belief_price)
    amount = str(to_u_unit(params.amount_bluna))
    return {
        "send": {
            "amount": amount,
            "contract": const.luna_bluna,
            "msg": msg
        }
    }


def get_buy_dict(belief_price: float, params: Params) -> Dict:
    amount = str(to_u_unit(params.amount_luna))
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
