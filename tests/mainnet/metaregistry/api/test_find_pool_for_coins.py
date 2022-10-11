import itertools

import ape

# NOTE: This is the most important method in the metaregistry contract since it will be used
# by integrators to find pools for coin pairs. It finds pools even if the coin pair is not
# a direct coin pair, but has a path through a metapool.


def _get_all_combinations(metaregistry, pool):

    pool_coins = [coin for coin in metaregistry.get_coins(pool) if coin != ape.utils.ZERO_ADDRESS]
    base_combinations = list(itertools.combinations(pool_coins, 2))
    all_combinations = base_combinations

    if metaregistry.is_meta(pool):
        underlying_coins = [
            coin
            for coin in metaregistry.get_underlying_coins(pool)
            if coin != ape.utils.ZERO_ADDRESS
        ]
        all_combinations = all_combinations + [
            (pool_coins[0], coin) for coin in underlying_coins if pool_coins[0] != coin
        ]

    return all_combinations


def test_all(populated_metaregistry, pool):

    combinations = _get_all_combinations(populated_metaregistry, pool)
    for combination in combinations:
        pools_containing_pair = populated_metaregistry.find_pools_for_coins(*combination)
        assert pool in pools_containing_pair

        for i, found_pool in enumerate(pools_containing_pair):
            assert populated_metaregistry.find_pool_for_coins(*combination, i) == found_pool
