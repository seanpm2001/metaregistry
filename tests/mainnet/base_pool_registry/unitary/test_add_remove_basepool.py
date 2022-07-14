import brownie

from tests.utils.constants import (
    BTC_BASEPOOL_LP_TOKEN_MAINNET,
    BTC_BASEPOOL_MAINNET,
    DAI,
    RENBTC,
    SBTC,
    TRIPOOL,
    TRIPOOL_LPTOKEN,
    USDC,
    USDT,
    WBTC,
)


def test_revert_add_base_pool_if_user_is_not_admin(base_pool_registry, charlie):

    with brownie.reverts():
        base_pool_registry.add_base_pool(
            TRIPOOL,
            TRIPOOL_LPTOKEN,
            2,
            False,
            {"from": charlie},
        )


def test_revert_add_nonexistent_base_pool(base_pool_registry, owner):

    with brownie.reverts():
        base_pool_registry.add_base_pool(
            DAI,  # should be a pool
            TRIPOOL_LPTOKEN,
            2,
            False,
            {"from": owner},
        )


def test_add_basepool(base_pool_registry, owner):

    base_pool_count = base_pool_registry.base_pool_count()

    base_pool_registry.add_base_pool(
        TRIPOOL,
        TRIPOOL_LPTOKEN,
        3,
        False,
        {"from": owner},
    )

    assert base_pool_registry.base_pool_count() == base_pool_count + 1
    assert base_pool_registry.get_base_pool_for_lp_token(TRIPOOL_LPTOKEN) == TRIPOOL
    assert base_pool_registry.get_lp_token(TRIPOOL) == TRIPOOL_LPTOKEN
    assert not base_pool_registry.is_legacy(TRIPOOL)
    assert not base_pool_registry.is_v2(TRIPOOL)
    assert not base_pool_registry.is_lending(TRIPOOL)

    base_pool_coins = base_pool_registry.get_coins(TRIPOOL)
    assert base_pool_coins[0] == DAI
    assert base_pool_coins[1] == USDC
    assert base_pool_coins[2] == USDT
    assert base_pool_coins[3] == brownie.ZERO_ADDRESS
    assert base_pool_registry.get_n_coins(TRIPOOL) == 3

    base_pool_coin_decimals = base_pool_registry.get_decimals(TRIPOOL)
    assert base_pool_coin_decimals[0] == 18
    assert base_pool_coin_decimals[1] == 6
    assert base_pool_coin_decimals[2] == 6


def test_add_basepool_with_legacy_abi(base_pool_registry, owner):

    base_pool_registry.add_base_pool(
        BTC_BASEPOOL_MAINNET,
        BTC_BASEPOOL_LP_TOKEN_MAINNET,
        3,
        True,
        {"from": owner},
    )

    assert base_pool_registry.is_legacy(BTC_BASEPOOL_MAINNET)

    base_pool_coins = base_pool_registry.get_coins(BTC_BASEPOOL_MAINNET)
    assert base_pool_coins[0] == RENBTC
    assert base_pool_coins[1] == WBTC
    assert base_pool_coins[2] == SBTC
    assert base_pool_coins[3] == brownie.ZERO_ADDRESS
    assert base_pool_registry.get_n_coins(BTC_BASEPOOL_MAINNET) == 3
