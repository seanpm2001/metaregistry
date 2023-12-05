from os import path
from typing import Union

import boa
from boa.vyper.contract import VyperContract
from eth.codecs.abi.exceptions import DecodeError as ABIDecodeError
from eth_account.signers.local import LocalAccount

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
BASE_DIR = path.join(path.dirname(path.abspath(__file__)), "..")


def get_contract_pools(contract_name: str, address: str) -> list[str]:
    """
    Retrieves the list of pools from a deployed contract with the given address.
    :param contract_name: The name of the contract to load.
    :param address: The address of the deployed contract.
    """
    registry = get_deployed_contract(contract_name, address)
    return [registry.pool_list(i) for i in range(registry.pool_count())]


def get_deployed_contract(contract_name: str, address: str) -> VyperContract:
    """
    Loads a contract and retrieves a deployed instance of it with the given address.
    TODO: Refactor calls to use fixtures instead of re-loading multiple times.
    :param contract_name: The name of the contract ABI to load.
    :param address: The address of the deployed contract.
    """
    file_name = path.join(
        BASE_DIR, f"contracts/interfaces/{contract_name}.json"
    )
    return boa.load_abi(file_name).at(address)


def deploy_contract(
    contract: str,
    *args,
    sender: Union[LocalAccount, str],
    directory: str = ".",
    **kwargs,
) -> VyperContract:
    file_name = path.join(
        BASE_DIR, f"contracts/mainnet/{directory}/{contract}.vy"
    )
    with boa.env.sender(sender):
        return boa.load(file_name, *args, **kwargs)


def check_decode_error(e: ABIDecodeError):
    """
    Checks that the error message is the expected decode error.
    This seems to be happening in some pools, but it's not clear if it's a boa or contract issue.
    :param e: The error to check.
    """
    assert e.msg == "Value length is not the expected size of 32 bytes"
    assert len(e.value) == 4096


def assert_negative_coin_balance(metaregistry, pool):
    """
    The implementation of get_balance calculates (balance - admin_balance) but sometimes the coin
    balance might be lower than the admin balance, resulting in an uint underflow.
    """
    coins = [
        coin for coin in metaregistry.get_coins(pool) if coin != ZERO_ADDRESS
    ]
    coin_balances = [
        get_deployed_contract("ERC20", coin).balanceOf(pool) for coin in coins
    ]
    admin_balances = metaregistry.get_admin_balances(pool)
    assert any(
        coin_balance < admin_balance
        for coin_balance, admin_balance in zip(coin_balances, admin_balances)
    )
