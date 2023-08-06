#!/usr/bin/python

import re
from wicc.waykicoin import WaykiCoin
from wicc.transactions import *
from wicc.serializer import Serializer, Stamper
from cryptos.mnemonic import *

# import re
# from cryptos import *
# def mySplit2(str):
#     t = str.upper()
#     p = re.compile('.{1,2}')  # 匹配任意字符1-2次
#     list = [int(x, 16)  for x in p.findall(t)]
#     new = []
#     for i in list:
#         if i > 128:
#             new.append(i-256)
#         else:
#             new.append(i)
#     print(new)
#     print("长度{}".format(len(new)))


class Wallet(object):

    # @classmethod
    # def generate_mnemonics(cls):
    #     return entropy_to_words(os.urandom(20))
    #
    # @classmethod
    # def private_key_from_mnemonics(cls, mnemonics):
    #     seed = mnemonic_to_seed(mnemonics)
    #     mainkey = bip32_master_key(seed, b"m/44'/99999'/0/0/0")
    #     print(mainkey)
    #     return ""
    #
    # @classmethod
    # def wallet_from_mnemonics(cls, mnemonics, main_net=False):
    #     private_key = cls.private_key_from_mnemonics(mnemonics)
    #     return Wallet(private_key=private_key, main_net=main_net)

    def __init__(self, private_key, main_net=False):
        """
        :param private_key: 私钥
        :param mainnet: 网络参数
        """
        chain_coin = WaykiCoin(testnet=not main_net)
        self.private_key = private_key
        self.public_key = chain_coin.privtopub(private_key)
        self.wallet_address = chain_coin.pubtoaddr(self.public_key)
        self.hash_code = chain_coin.hashcode
        self.version = 1

    def transfer_tx(self, transfer: TransferTransaction) -> str:
        """
        :param transfer: 转账交易
        :return: 签名后的转账交易
        """
        ser_message = Serializer()\
            .ser_version(self.version)\
            .ser_tx_type(TxType.U_COIN_TRANSFER.value)\
            .ser_valid_height(transfer.valid_height)\
            .ser_regid_or_public_key(transfer.register_id, self.public_key)\
            .ser_fee(transfer.fee_amount, transfer.fee_coin_symbol)\
            .ser_transfer(transfer.transfer_list)\
            .ser_memo(transfer.memo)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer()\
            .ser_tx_type(TxType.U_COIN_TRANSFER.value)\
            .ser_version(self.version)\
            .ser_valid_height(transfer.valid_height)\
            .ser_regid_or_public_key(transfer.register_id, self.public_key) \
            .ser_fee(transfer.fee_amount, transfer.fee_coin_symbol)\
            .ser_transfer(transfer.transfer_list)\
            .ser_memo(transfer.memo)\
            .ser_signature(signature)\
            .to_hex_string()

    # def vote_tx(self, vote: VoteTransaction) -> str:
    #     """
    #     :param vote: 投票交易
    #     :return: 签名后的 投票交易 信息
    #     """
    #     pass
    #
    # def contract_deploy_tx(self, contract_deploy: ContractDeployTransaction) -> str:
    #     """
    #     :param contract_deploy: 合约部署交易
    #     :return: 签名后的 合约部署交易 信息
    #     """

    def contract_call_tx(self, contract_call: ContractCallTransaction) -> str:
        """
        :param contract_call: 合约调用交易
        :return: 签名后的 合约调用交易
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.U_CONTRACT_INVOKE.value) \
            .ser_valid_height(contract_call.valid_height) \
            .ser_regid_or_public_key(contract_call.register_id, self.public_key) \
            .ser_regid(contract_call.app_id)\
            .ser_contract_message(contract_call.contract_call_msg)\
            .ser_fee_amount(contract_call.fee_amount)\
            .ser_coin_symbol(contract_call.fee_coin_symbol) \
            .ser_amount(contract_call.pay_amount, contract_call.pay_coin_symbol)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.U_CONTRACT_INVOKE.value) \
            .ser_version(self.version) \
            .ser_valid_height(contract_call.valid_height) \
            .ser_regid_or_public_key(contract_call.register_id, self.public_key) \
            .ser_regid(contract_call.app_id)\
            .ser_contract_message(contract_call.contract_call_msg)\
            .ser_fee_amount(contract_call.fee_amount) \
            .ser_coin_symbol(contract_call.fee_coin_symbol) \
            .ser_amount(contract_call.pay_amount, contract_call.pay_coin_symbol)\
            .ser_signature(signature)\
            .to_hex_string()

    def dex_limited_price_buy_tx(self, t: DexLimitedPriceBuyTransaction):
        """
        :param t: dex限价买单
        :return: 签名后的 dex限价买单
        """
        ser_message = Serializer()\
            .ser_version(self.version)\
            .ser_tx_type(TxType.DEX_LIMITED_PRICE_BUY_ORDER.value)\
            .ser_valid_height(t.valid_height)\
            .ser_regid_or_public_key(t.register_id, self.public_key)\
            .ser_fee(t.fee_amount, t.fee_coin_symbol)\
            .ser_coin_symbol(t.coin_symbol)\
            .ser_coin_symbol(t.asset_symbol)\
            .ser_coin_amount(t.asset_amount)\
            .ser_coin_amount(t.price)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.DEX_LIMITED_PRICE_BUY_ORDER.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .ser_coin_amount(t.price) \
            .ser_signature(signature) \
            .to_hex_string()

    def dex_limited_price_sell_tx(self, t: DexLimitedPriceSellTransaction):
        """
        :param t: dex限价卖单
        :return: 签名后的 dex限价卖单
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.DEX_LIMITED_PRICE_SELL_ORDER.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .ser_coin_amount(t.price) \
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.DEX_LIMITED_PRICE_SELL_ORDER.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .ser_coin_amount(t.price) \
            .ser_signature(signature) \
            .to_hex_string()

    def dex_market_price_buy_tx(self, t: DexMarketPriceBuyTransaction):
        """
        :param t: dex市价买单
        :return: 签名后的 dex市价买单
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.DEX_MARKET_PRICE_BUY_ORDER.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.DEX_MARKET_PRICE_BUY_ORDER.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .ser_signature(signature) \
            .to_hex_string()

    def dex_market_price_sell_tx(self, t: DexMarketPriceBuyTransaction):
        """
        :param t: dex市价卖单
        :return: 签名后的 dex市价卖单
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.DEX_MARKET_PRICE_SELL_ORDER.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.DEX_MARKET_PRICE_SELL_ORDER.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_coin_amount(t.asset_amount) \
            .ser_signature(signature) \
            .to_hex_string()

    def dex_cancel_order_tx(self, t: DexCancelOrderTransaction):
        """
        :param t: dex取消订单
        :return: 签名后的 dex取消订单
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.DEX_CANCEL_ORDER.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_order_id(t.order_id)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer()\
            .ser_tx_type(TxType.DEX_CANCEL_ORDER.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_order_id(t.order_id) \
            .ser_signature(signature) \
            .to_hex_string()

    def cdp_stake_tx(self, t: CdpStakeTransaction):
        """
        :param t: 创建/追加cdp交易
        :return: 签名后的 创建/追加cdp交易
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.CDP_STAKE.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id)\
            .ser_cdp_stake_list(t.stake_list)\
            .ser_coin_symbol(t.get_coin_symbol)\
            .ser_coin_amount(t.get_amount)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer()\
            .ser_tx_type(TxType.CDP_STAKE.value)\
            .ser_version(self.version)\
            .ser_valid_height(t.valid_height)\
            .ser_regid_or_public_key(t.register_id, self.public_key)\
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id) \
            .ser_cdp_stake_list(t.stake_list)\
            .ser_coin_symbol(t.get_coin_symbol)\
            .ser_coin_amount(t.get_amount)\
            .ser_signature(signature)\
            .to_hex_string()

    def cdp_redeem_tx(self, t: CdpRedeemTransaction):
        """
        :param t: 赎回cdp交易
        :return: 签名后的 赎回cdp交易
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.CDP_REDEEM.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id) \
            .ser_coin_amount(t.repay_amount) \
            .ser_cdp_redeem_list(t.redeem_list) \
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.CDP_REDEEM.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id) \
            .ser_coin_amount(t.repay_amount) \
            .ser_cdp_redeem_list(t.redeem_list) \
            .ser_signature(signature) \
            .to_hex_string()

    def cdp_liquidate_tx(self, t: CdpLiquidateTransaction):
        """
        :param t: 清算cdp交易
        :return: 签名后的 清算cdp交易
        """
        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.CDP_LIQUIDATE.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id) \
            .ser_coin_symbol(t.liquidate_coin_symbol) \
            .ser_coin_amount(t.liquidate_amount)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.CDP_LIQUIDATE.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid_or_public_key(t.register_id, self.public_key) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_cdp_id(t.cdp_id) \
            .ser_coin_symbol(t.liquidate_coin_symbol) \
            .ser_coin_amount(t.liquidate_amount) \
            .ser_signature(signature) \
            .to_hex_string()

    def asset_publish_tx(self, t: AssetPublishTransaction) -> str:
        """
        :param t: 资产发布交易
        :return: 签名后的 资产发布交易
        """
        if not re.match(r"[A-Z]{6,7}$", t.asset_symbol):
            raise Exception("Asset symbol Error")

        ser_message = Serializer() \
            .ser_version(self.version) \
            .ser_tx_type(TxType.ASSET_UPDATE.value) \
            .ser_valid_height(t.valid_height) \
            .ser_regid(t.register_id) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_asset_type_and_value(t.asset_update_type, t.asset_update_value)\
            .to_message()

        signature = Stamper.stamp(ser_message, self.private_key)

        return Serializer() \
            .ser_tx_type(TxType.ASSET_UPDATE.value) \
            .ser_version(self.version) \
            .ser_valid_height(t.valid_height) \
            .ser_regid(t.register_id) \
            .ser_fee(t.fee_amount, t.fee_coin_symbol) \
            .ser_coin_symbol(t.asset_symbol) \
            .ser_asset_type_and_value(t.asset_update_type, t.asset_update_value) \
            .ser_signature(signature) \
            .to_hex_string()

if __name__ == '__main__':
    s = ['slow', 'rail', 'time', 'toss', 'daring', 'proof', 'yard', 'another', 'olive', 'special', 'magnet', 'fly', 'busy', 'tent', 'stove']
    print(Wallet.private_key_from_mnemonics(s))