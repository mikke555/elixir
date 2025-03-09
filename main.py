from random import shuffle

import questionary

from modules.config import logger
from modules.elixir import Elixir
from modules.utils import sleep
from settings import *


def get_action() -> str:
    choices = [
        questionary.Choice("Withdraw deUSD", "withdraw"),
        questionary.Choice("Commit to convert elxETH > deUSD", "commit"),
        questionary.Choice("Quit", "quit"),
    ]

    style = questionary.Style(
        [
            ("qmark", "fg:#47A6F9 bold"),
            ("pointer", "fg:#47A6F9 bold"),
            ("selected", "fg:#47A6F9"),
            ("highlighted", "fg:#808080"),
            ("answer", "fg:#808080 bold"),
            ("instruction", "fg:#8c8c8c italic"),
        ]
    )

    action = questionary.select(
        "Action",
        choices=choices,
        style=style,
    ).ask()

    if action == "quit" or action == None:
        quit()

    return action


def get_accounts():
    with open("keys.txt", "r") as f:
        keys = [row.strip() for row in f]

    if SHUFFLE_WALLETS:
        shuffle(keys)

    return keys


def main(action, accounts):
    total = len(accounts)

    for index, key in enumerate(accounts, start=1):
        counter_str = f"[{index}/{total}]"
        elixir = Elixir(key, counter_str)

        if action == "commit":
            tx_status = elixir.commit_DeUSD()
        if action == "withdraw":
            tx_status = elixir.withdraw_deUSD()

        if tx_status and index < total:
            sleep(*SLEEP_BETWEEN_WALLETS)


if __name__ == "__main__":
    try:
        action = get_action()
        accounts = get_accounts()

        main(action, accounts)

    except KeyboardInterrupt:
        logger.warning("Cancelled by user")
    except Exception as err:
        logger.error(f"An error occured: {err}")
