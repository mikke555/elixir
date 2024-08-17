import random
import time

from eth_account import Account
from web3 import Web3

from modules.config import CHAIN_DATA, ERC20_ABI, logger
from settings import *


class Wallet:
    def __init__(self, private_key, counter, chain):
        self.private_key = private_key
        self.account = Account.from_key(private_key)
        self.address = self.account.address

        self.web3 = Web3(Web3.HTTPProvider(CHAIN_DATA[chain]["rpc"]))
        self.explorer = CHAIN_DATA[chain]["explorer"]

        self.counter = counter
        self.module_str = f"{self.counter} {self.address} | "

    def __str__(self):
        return f"Wallet(address={self.address})"

    def get_eth_balance(self):
        return self.web3.eth.get_balance(self.address)

    def get_contract(self, address, abi=None):
        contract_address = Web3.to_checksum_address(address)
        if not abi:
            abi = ERC20_ABI

        return self.web3.eth.contract(address=contract_address, abi=abi)

    def get_contract_funcs(self, abi):
        functions = [func["name"] for func in abi if func["type"] == "function"]

        print("Available functions in the contract: \n")
        for func in functions:
            print(func)

    def get_contract_funcs_with_args(self, abi):
        print("Available functions in the contract: \n")
        for func in abi:
            if func["type"] == "function":
                func_name = func["name"]
                inputs = func["inputs"]
                args_str = ", ".join(
                    [f"{input['type']} {input['name']}" for input in inputs]
                )
                print(f"{func_name}({args_str})")

    def get_tx_data(self, value=0, **kwargs):
        return {
            "chainId": self.web3.eth.chain_id,
            "from": self.address,
            "nonce": self.web3.eth.get_transaction_count(self.address),
            "value": value,
            # "gasPrice": self.web3.eth.gas_price,
            **kwargs,
        }

    def send_tx(self, tx, tx_label=""):
        try:
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info(f"{tx_label} | {self.explorer}/tx/{tx_hash.hex()}")

            tx_receipt = self.web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=400
            )

            if tx_receipt.status == 1:
                logger.success(f"{tx_label} | Tx confirmed \n")
                return tx_receipt.status
            else:
                raise ValueError("Tx failed \n")

        except Exception as error:
            logger.error(f"error: {error}")

    def get_balance(self, token_addr):
        token = self.get_contract(token_addr)

        balance = token.functions.balanceOf(self.address).call()
        decimals = token.functions.decimals().call()
        symbol = token.functions.symbol().call()

        return balance, decimals, symbol

    def check_allowance(self, token_addr, spender):
        token = self.get_contract(token_addr)

        return token.functions.allowance(self.address, spender).call()

    def approve(self, token_address, spender, tx_label):
        token = self.get_contract(token_address)

        balance, decimals, symbol = self.get_balance(token_address)
        allowance = self.check_allowance(token_address, spender)

        if balance == 0:
            logger.info(f"{tx_label} | Your {symbol} is 0")
            return

        if allowance >= balance:
            logger.info(
                f"{tx_label} | {balance / 10 ** decimals} {symbol} already approved"
            )
            return

        tx_data = self.get_tx_data()
        tx = token.functions.approve(spender, balance).build_transaction(tx_data)

        status = self.send_tx(tx, tx_label)
        time.sleep(random.uniform(5, 15))
        return status
