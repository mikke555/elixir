import json
from sys import stderr

from loguru import logger
from web3 import Web3

logger.remove()
logger.add(
    stderr,
    format="<white>{time:HH:mm:ss}</white> | <level>{message}</level>",
)

CHAIN_DATA = {
    "ethereum": {
        "rpc": "https://rpc.ankr.com/eth",
        "explorer": "https://etherscan.io",
        "token": "ETH",
        "chain_id": 1,
    },
}

mainnet_client = Web3(Web3.HTTPProvider(CHAIN_DATA["ethereum"]["rpc"]))


with open("data/abi/erc20.json") as f:
    ERC20_ABI = json.load(f)

with open("data/abi/elixir.json") as f:
    ELIXIR_ABI = json.load(f)
