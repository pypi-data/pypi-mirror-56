#!/usr/bin/python
# -*- coding: utf-8 -*-
from cryptos.coins.base import BaseCoin
from cryptos.transaction import *

class WaykiCoin(BaseCoin):
    coin_symbol = "WICC"
    display_name = "WaykiChain"
    enabled = True
    magicbyte = 73
    script_magicbyte = 51
    testnet_overrides = {
        'display_name': "WaykiChain Testnet",
        'coin_symbol': "wicc",
        'magicbyte': 135,
        'script_magicbyte': 88,
        # 'hashcode': 2
    }

