

# 维基链钱包工具SDK (WaykiChain Wallet Utilities SDK)


## 核心功能 (Core Functions)

- 创建钱包 (Create Wallet)
- 交易离线签名 (Offline Transaction Signing)
- 与节点交互 (Interaction with nodes)

## 使用方式（Usage）

### 交易离线签名 (Offline Transaction Signing)

#### 1. 转账交易（WaykiChain Create Wallet）

##### 生成私钥 (Generate private key)
```
from wicc.wallet import Wallet

Wallet.generate_private_key(main_net=False)

Wallet.generate_private_key(main_net=True)

```

#### 2. 转账交易（Transfer Transaction）
##### 多币种转账交易 (Sign UCoinTransfer Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet
from wicc.baas.manager import BaasManager

tr = TransferTransaction()
tr.valid_height = BaasManager.get_valid_height()
tr.register_id = "265866-2" // 非必填项
tr.fee_amount = 10000000
tr.fee_coin_symbol = "WICC"
tr.memo = "转账"
    tr.transfer_list = [
		Transfer(amount=10000000000, symbol="WICC", > desert_address="wahso3aWQFtFpmaTmFF8FFYbiM88xE4R4h"),
		Transfer(amount=10000000000, symbol="WICC", desert_address="wMS4ZG4xfoTY9MXpbykTPvFPzFViPa6aGf"),
    ]

w = Wallet("Private Key", mainnet=False)
rawtx = w.transfer_tx(tr)
print(BaasManager.send_transfer_tx(rawtx))
```
#### 3. 合约交易（Contract Transaction）
##### 多币种合约调用交易 (Sign Invoke Contract Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet
from wicc.baas.manager import BaasManager

w = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")
contract_call = ContractCallTransaction()
contract_call.valid_height = BaasManager.get_valid_height()
contract_call.register_id = "0-1"
contract_call.fee_amount = 100000
contract_call.fee_coin_symbol = CoinType.WICC.value
contract_call.app_id = "450687-1"
contract_call.contract_call_msg = "f001"
contract_call.pay_coin_symbol = CoinType.WUSD.value
contract_call.pay_amount = 100000000
contract_call_rawtx = w.contract_call_tx(contract_call)
print(contract_call_rawtx)
```

#### 4. CDP Transaction
##### CDP抵押交易签名 (Sign Cdp Stake Transaction)
```
wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")

tr = CdpStakeTransaction()
tr.valid_height = 5003
tr.fee_amount = 10000000
tr.register_id = "0-1"
tr.fee_coin_symbol = CoinType.WUSD.value
tr.stake_list = [CdpStakeAsset(CoinType.WICC.value, 100000000)]
tr.cdp_id = "009c0e665acdd9e8ae754f9a51337b85bb8996980a93d6175b61edccd3cdc144"
tr.get_coin_symbol = CoinType.WUSD.value
tr.get_amount = 50000000
raw_tx = wallet.cdp_stake_tx(tr)
print(raw_tx)
```

##### CDP赎回 (Sign Cdp Redeem Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")

tr = CdpRedeemTransaction()
tr.valid_height = 8510
tr.register_id = "0-1"
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.redeem_list = [CdpRedeemAsset(CoinType.WICC.value, 100000000)]
tr.cdp_id = "009c0e665acdd9e8ae754f9a51337b85bb8996980a93d6175b61edccd3cdc144"
tr.repay_amount = 50000000
raw_tx = wallet.cdp_redeem_tx(tr)
print(raw_tx)
```

##### CDP清算 (Sign CDP Liquidate Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")

tr = CdpLiquidateTransaction()
tr.valid_height = 283308
tr.register_id = "0-1"
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.cdp_id = "009c0e665acdd9e8ae754f9a51337b85bb8996980a93d6175b61edccd3cdc144"
tr.liquidate_amount = 10000000
tr.liquidate_coin_symbol = CoinType.WICC.value
raw_tx = wallet.cdp_liquidate_tx(tr)
print(raw_tx)
```

#### 5. DEX (WaykiChain Decentralized Exchange) Transaction
##### 限价买单交易 (Sign Dex Sell Limit Transaction)

```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")

tr = DexLimitedPriceBuyTransaction()
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.valid_height = 283308
tr.register_id = "0-1"
tr.coin_symbol = CoinType.WUSD.value
tr.asset_symbol = CoinType.WICC.value
tr.asset_amount = 100 * 100000000
tr.price = 10 * 10000
rawtx = wallet.dex_limited_price_buy_tx(tr)
print(rawtx)

```
##### 限价卖单交易 (Sign Dex Buy Limit Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")
tr = DexLimitedPriceSellTransaction()
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.valid_height = 283308
tr.register_id = "0-1"
tr.coin_symbol = CoinType.WUSD.value
tr.asset_symbol = CoinType.WICC.value
tr.asset_amount = 100 * 100000000
tr.price = 1 * 10000
rawtx = wallet.dex_limited_price_sell_tx(tr)
print(rawtx)
```

##### 市价买单交易 (Sign Dex Market Buy Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")
tr = DexMarketPriceBuyTransaction()
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.valid_height = 283308
tr.register_id = "0-1"
tr.coin_symbol = CoinType.WUSD.value
tr.coin_amount = 100 * 100000000
tr.asset_symbol = CoinType.WICC.value
rawtx = wallet.dex_market_price_buy_tx(tr)
print(rawtx)
```

##### 市价卖单交易 (Sign Dex Market Sell Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")
tr = DexMarketPriceSellTransaction()
tr.fee_amount = 10000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.valid_height = 283308
tr.register_id = "0-1"
tr.coin_symbol = CoinType.WUSD.value
tr.asset_symbol = CoinType.WICC.value
tr.asset_amount = 100 * 100000000
rawtx = wallet.dex_market_price_sell_tx(tr)
print(rawtx)

```

##### 取消挂单交易 (Sign Dex Cancel Transaction)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y9XMqNzseQFSK32SvMDNF9J7xz1CQmHRsmY1hMYiqZyTck8pYae3")
tr = DexCancelOrderTransaction()
tr.fee_amount = 1000000
tr.fee_coin_symbol = CoinType.WICC.value
tr.valid_height = 283308
tr.register_id = "0-1"
tr.order_id = "009c0e665acdd9e8ae754f9a51337b85bb8996980a93d6175b61edccd3cdc144"
rawtx = wallet.dex_cancel_order_tx(tr)
print(rawtx)

```

#### 5. 资产相关 (Assets Transaction)

##### 资产发布 (Publish assets)
```
from wicc.transactions import *
from wicc.wallet import Wallet

wallet = Wallet("Y6J4aK6Wcs4A3Ex4HXdfjJ6ZsHpNZfjaS4B9w7xqEnmFEYMqQd13")
tr = AssetPublishTransaction()
tr.valid_height = 11443
tr.fee_amount = 1000000
tr.register_id = "0-1"
tr.fee_coin_symbol = CoinType.WICC.value
tr.asset_update_type = AssetUpdateType.OWNER_UID.value
tr.asset_update_value = "0-2"
tr.asset_symbol = "STOOOOO"

raw_tx = wallet.asset_publish_tx(tr)
```

### 与节点交互 (Interaction with nodes)

#### 1. 获取当前高度 (Get valid height)
```
from wicc.baas.manager import BaasManager

height = BaasManager.set_net(is_main_net=False).get_valid_height()

```

#### 2. 提交签名 (Submit Transaction)
```
from wicc.baas.manager import BaasManager

raw_tx = ""
BaasManager.set_net(is_main_net=False).send_tx(raw_tx)

```

## 引用项目 (Reference Projects)
[Cryptos](https://pypi.org/project/cryptos/)

