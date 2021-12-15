from terra_sdk.client.lcd import LCDClient
from src import const

def get_bluna_for_luna(terra: LCDClient):
    return_amount = terra.wasm.contract_query(const.luna_bluna, {
        "simulation": {
            "offer_asset": {
                "info": {
                    "native_token": {
                        "denom": const.uluna
                    }
                },
                "amount": "10000000"
            }}
    })['return_amount']

    print(return_amount)
