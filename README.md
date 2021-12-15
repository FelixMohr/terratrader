# terratrader

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)


<div align="center">
<img
    width=616px
    src="files/moon.jpeg"
    alt="to the moon"
/>
</div>
<br />
<br />

## What it does
This bot can perform [Terraswap](https://app.terraswap.io) trades for you. It trades on the [Luna/bLuna](https://finder.extraterrestrial.money/mainnet/address/terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p) pair.

## Installation
1. Create  virtual environment: `python -m venv venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`

## Using it

Set the environment variables:
* `PK` private key of your wallet to trade with (read section below on how to find it)

Then execute the following commands:

1. `. venv/bin/activate` (if not done yet)
2. `python cli.py` will start the CLI


### Commands
* `price`: Show price for selling/buying
* `amount-luna`: Set the luna amount for buying bLuna
* `amount-bluna`: Set the bLuna amount for selling bLuna
* `inv-sell-price`: Sets the price for when to sell bLuna
* `buy-price`: Sets the price for when to buy bLuna
* `spread`: Sets the maximum spread (default 0,5%)
* `mode-buy`: Sets the bot to buying mode (will toggle automatically when bought)
* `mode-sell`: Sets the bot to selling mode (will toggle automatically when sold)
* `buy`: Manually buys bLuna
* `sell`: Manually sells bLuna
* `bot`: Starts the bot. Stop it with [Ctrl]+[C]

## Finding your private key
1. Export the "private key" in your Terra Station
2. Decode this base64 string and take the encoded key from the dict
3. `npm install -g crypto-js`
4. `export NODE_PATH=/usr/local/lib/node_modules` (check that the path is correct, may need to delete "local")
5. `node scripts/decode_pk.js [ENCODED_PK] [WALLET_PASSWORD]`
