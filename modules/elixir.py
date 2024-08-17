from modules.config import ELIXIR_ABI, logger
from modules.utils import check_gas
from modules.wallet import Wallet


class Elixir(Wallet):
    def __init__(self, private_key, counter):
        super().__init__(private_key, counter, chain="ethereum")
        self.module_str += "Elixir |"
        self.contract = self.get_contract(
            address="0x652329cc4F00Af06a8020B41846d54a439A64620", abi=ELIXIR_ABI
        )

    def get_uncommitted_balance(self):
        return int(self.contract.functions.uncommittedBalance(self.address).call())

    @check_gas
    def commit_DeUSD(self):
        balance = self.get_uncommitted_balance()

        if balance == 0:
            logger.debug(f"{self.module_str} No balance to commit, skipping \n")
            return

        try:
            contract_tx = self.contract.functions.commitDeUSD(
                balance
            ).build_transaction(self.get_tx_data())

        except Exception as error:
            print(f"error building tx: {error}")

        return self.send_tx(
            contract_tx,
            tx_label=f"{self.module_str} commit {self.web3.from_wei(balance, 'ether')} elxETH to DeUSD",
        )
