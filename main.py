from random import shuffle

from modules.config import logger
from modules.elixir import Elixir
from modules.utils import sleep
from settings import *


if __name__ == "__main__":
    try:
        with open("keys.txt", "r") as f:
            keys = [row.strip() for row in f]

        if SHUFFLE_WALLETS:
            shuffle(keys)

        total_keys = len(keys)

        logger.success(f"Loaded {total_keys} wallet(s) \n")

        input("Press Enter to run the script... \n")

        for index, key in enumerate(keys, start=1):
            counter_str = f"[{index}/{total_keys}]"

            elixir = Elixir(key, counter_str)
            tx_status = elixir.commit_DeUSD()

            if tx_status and index < total_keys:
                sleep(*SLEEP_BETWEEN_WALLETS)

        logger.success('All accounts done \n')
        input('> Exit')

    except KeyboardInterrupt:
        logger.warning("Script interrupted by user")
