import random
import time
from datetime import datetime

from tqdm import tqdm

from modules.config import logger, mainnet_client
from settings import *


def sleep(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    desc = datetime.now().strftime("%H:%M:%S")

    for _ in tqdm(
        range(x), desc=desc, bar_format="{desc} | Sleeping {n_fmt}/{total_fmt}"
    ):
        time.sleep(1)
    print()


def get_gas():
    try:
        gas_price = mainnet_client.eth.gas_price
        gwei = mainnet_client.from_wei(gas_price, "gwei")
        return gwei
    except Exception as error:
        logger.error(error)


def wait_gas():
    while True:
        gas = get_gas()

        if gas > MAX_GWEI:
            logger.info(f"Current gwei {gas} > {MAX_GWEI}")
            sleep(60,60)
        else:
            break


def check_gas(func):
    def wrapper(*args, **kwargs):
        wait_gas()
        return func(*args, **kwargs)

    return wrapper
