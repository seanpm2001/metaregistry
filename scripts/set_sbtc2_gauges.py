from brownie import (
    Contract,
    ZERO_ADDRESS,
    accounts,
    network,
)

from brownie.network.gas.strategies import GasNowScalingStrategy

ADDRESS_PROVIDER = "0x0000000022D53366457F9d5E68Ec105046FC4383"
txparams = {
    "from": accounts.at(
        "0xbabe61887f1de2713c6f97e567623453d3C79f67", force=True
    )
}

def init_contract(contract_addr: str):
    try:
        return Contract(contract_addr)
    except:
        return Contract.from_explorer(contract_addr)


if network.show_active() == "mainnet":
    print("Deploying on mainnet")
    accounts.load("babe")
    txparams = {"from": accounts[0], "required_confs": 5}
    try:
        network.gas_price(GasNowScalingStrategy("slow", "fast"))
    except ConnectionError:
        pass
    

POOL_DATA = {
    "pool": "0xf253f83AcA21aAbD2A20553AE0BF7F65C755A07F",
    "lp_token": "0x051d7e5609917Bd9b73f04BAc0DED8Dd46a74301",
    "num_coins": 2,
    "is_legacy": False,
    "is_lending": False,
    "is_v2": True,
    "gauge": "0x6D787113F23bED1D5e1530402B3f364D0A6e5Af3"
}
    

def main():

    # admin only: only admin of ADDRESSPROVIDER's proxy admin can do the following:
    address_provider = init_contract(ADDRESS_PROVIDER)
    address_provider_admin = address_provider.admin()
    proxy_admin = init_contract(address_provider_admin)
    base_pool_registry = init_contract("0xDE3eAD9B2145bBA2EB74007e58ED07308716B725")
    stable_registry = init_contract("0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5")
    metaregistry = init_contract("0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC")
    
    # --- add base pool to base pool registry ---
    call_data = base_pool_registry.add_base_pool.encode_input(
            POOL_DATA["pool"],
            POOL_DATA["lp_token"],
            POOL_DATA["num_coins"],
            POOL_DATA["is_legacy"],
            POOL_DATA["is_lending"],
            POOL_DATA["is_v2"],
        )

    proxy_admin.execute(base_pool_registry, call_data, txparams)
    base_pool_index = base_pool_registry.base_pool_count() - 1
    assert (
            base_pool_registry.base_pool_list(base_pool_index)
            == POOL_DATA["pool"]
        )
    
    # --- add base pool's gauge to base registry ---
    gauges = stable_registry.get_gauges(POOL_DATA["pool"])
    assert gauges[0][0] == ZERO_ADDRESS
    
    call_data = stable_registry.set_liquidity_gauges.encode_input(
        POOL_DATA["pool"],
        [POOL_DATA["gauge"]] + [ZERO_ADDRESS]*9
    )
    breakpoint()
    proxy_admin.execute(stable_registry, call_data, txparams)
    
    gauges = stable_registry.get_gauges(POOL_DATA["pool"])
    assert gauges[0][0] == POOL_DATA["gauge"] 

    # check if metaregistry has the gauge
    assert metaregistry.get_gauges(POOL_DATA["pool"])[0] == POOL_DATA["gauge"]
    print("success!")
