import terra_sdk
import sys

from src.core import get_bluna_for_luna_price, get_luna_for_bluna_price, buy, sell
from src.helpers import create_params, info, create_terra, create_wallet, warn, from_uluna, get_arg_safe
from src import bot, const


def main():
    with open("files/greeting.txt") as f:
        content = f.read()
        print(content)

    params, terra, wallet = setup()

    while True:
        inp = input(' 👽    >>> ').strip()
        split = inp.split()
        if not len(split):
            continue
        command = split[0]
        args = split[1:]
        if command == 'quit':
            terra.session.close()
            break
        try:
            if command == 'price':
                return_amount, price = get_bluna_for_luna_price(terra, params)
                info("returned for {} Luna: {} bLuna, price: {}".format(params.amount_luna, from_uluna(return_amount), price))
                return_amount, price = get_luna_for_bluna_price(terra, params)
                info("returned for {} bLuna: {} Luna, inv price: {}, price: {}".format(params.amount_bluna, from_uluna(return_amount), 1/price, price))
            elif command == 'amount-luna':
                amount_luna = get_arg_safe(args)
                if amount_luna:
                    params.amount_luna = float(amount_luna)
                    info("amount for selling Luna set to {}".format(params.amount_luna))
            elif command == 'amount-bluna':
                amount_luna = get_arg_safe(args)
                if amount_luna:
                    params.amount_bluna = float(amount_luna)
                    info("amount for selling bLuna set to {}".format(params.amount_bluna))
            elif command == 'inv-sell-price':
                inv_sell_price = get_arg_safe(args)
                if inv_sell_price:
                    params.inv_sell_price = float(inv_sell_price)
                    info("price for selling bLuna set to {}".format(params.inv_sell_price))
            elif command == 'buy-price':
                buy_price = get_arg_safe(args)
                if buy_price:
                    params.buy_price = float(buy_price)
                    info("price for buying bLuna set to {}".format(params.buy_price))
            elif command == 'spread':
                spread = get_arg_safe(args)
                if spread:
                    params.spread = float(spread)
                    info("max spread set to {}".format(params.spread))
            elif command == 'bot':
                bot.run(params, terra, wallet)
            elif command == 'mode-buy':
                params.mode = const.buy
                info("set mode to buy ({})".format(params.mode))
            elif command == 'mode-sell':
                params.mode = const.sell
                info("set mode to sell ({})".format(params.mode))
            elif command == 'buy':
                _, price = get_bluna_for_luna_price(terra, params)
                buy(params, terra, price, wallet)
            elif command == 'sell':
                _, price = get_luna_for_bluna_price(terra, params)
                sell(params, terra, price, wallet)
            else:
                info('Invalid Command.')
        except terra_sdk.exceptions.LCDResponseError as e:
            warn(str(e))


def setup():
    params = create_params()
    terra = create_terra()
    wallet = create_wallet(terra)
    return params, terra, wallet


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1 and args[1] == 'bot':
        params, terra, wallet = setup()
        # can't write persistent files in heroku
        params.never_log = True
        bot.run(params, terra, wallet)
    else:
        main()
