import click
from ape import project
from ape.cli import network_option, account_option, NetworkBoundCommand
from ape.utils import ZERO_ADDRESS

ADDRESS_PROVIDER = "0x0000000022D53366457F9d5E68Ec105046FC4383"
STABLE_REGISTRY_ADDRESS = "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5"
STABLE_FACTORY_ADDRESS = "0xB9fC157394Af804a3578134A6585C0dc9cc990d4"
CRYPTO_REGISTRY_ADDRESS = ""  # left blank because a new one gets deployed
CRYPTO_FACTORY_ADDRESS = "0xF18056Bbd320E96A48e3Fbf8bC061322531aac99"
BASE_POOLS = {
    "tripool" : {
        "pool": "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7",
        "lp_token": "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",
        "num_coins": 3,
        "is_legacy": False,
        "is_lending": False,
        "is_v2": False,
    },
    "fraxusdc" : {
        "pool": "0xdcef968d416a41cdac0ed8702fac8128a64241a2",
        "lp_token": "0x3175df0976dfa876431c2e9ee6bc45b65d3473cc",
        "num_coins": 2,
        "is_legacy": False,
        "is_lending": False,
        "is_v2": False,
    },
    "sbtc" : {
        "pool": "0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714",
        "lp_token": "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3",
        "num_coins": 3,
        "is_legacy": True,
        "is_lending": False,
        "is_v2": False,
    },
}
CRYPTO_REGISTRY_POOLS = {
    "tricrypto2" : {
        "pool": "0xD51a44d3FaE010294C616388b506AcdA1bfAAE46",
        "lp_token": "0xc4AD29ba4B3c580e6D59105FFf484999997675Ff",
        "gauge": "0xDeFd8FdD20e0f34115C7018CCfb655796F6B2168",
        "zap": "0x3993d34e7e99Abf6B6f367309975d1360222D446",
        "num_coins": 3,
        "name": "tricrypto2",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "eurt3crv" : {
        "pool": "0x9838eccc42659fa8aa7daf2ad134b53984c9427b",
        "lp_token": "0x3b6831c0077a1e44ed0a21841c3bc4dc11bce833",
        "gauge": "0x4Fd86Ce7Ecea88F7E0aA78DC12625996Fb3a04bC",
        "zap": "0x5D0F47B32fDd343BfA74cE221808e2abE4A53827",
        "num_coins": 2,
        "name": "eurtusd",
        "base_pool": BASE_POOLS["tripool"]["pool"],
        "has_positive_rebasing_tokens": False,
    },
    "eursusdc" : {
        "pool": "0x98a7F18d4E56Cfe84E3D081B40001B3d5bD3eB8B",
        "lp_token": "0x3D229E1B4faab62F621eF2F6A610961f7BD7b23B",
        "gauge": "0x65CA7Dc5CB661fC58De57B1E1aF404649a27AD35",
        "zap": ZERO_ADDRESS,
        "num_coins": 2,
        "name": "eursusd",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "crveth" : {
        "pool": "0x8301AE4fc9c624d1D396cbDAa1ed877821D7C511",
        "lp_token": "0xEd4064f376cB8d68F770FB1Ff088a3d0F3FF5c4d",
        "gauge": "0x1cEBdB0856dd985fAe9b8fEa2262469360B8a3a6",
        "zap": ZERO_ADDRESS,
        "num_coins": 2,
        "name": "crveth",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "cvxeth" : {
        "pool": "0xB576491F1E6e5E62f1d8F26062Ee822B40B0E0d4",
        "lp_token": "0x3A283D9c08E8b55966afb64C515f5143cf907611",
        "gauge": "0x7E1444BA99dcdFfE8fBdb42C02F0005D14f13BE1",
        "zap": ZERO_ADDRESS,
        "num_coins": 2,
        "name": "cvxeth",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "xaut3crv" : {
        "pool": "0xAdCFcf9894335dC340f6Cd182aFA45999F45Fc44",
        "lp_token": "0x8484673cA7BfF40F82B041916881aeA15ee84834",
        "gauge": "0x1B3E14157ED33F60668f2103bCd5Db39a1573E5B",
        "zap": "0xc5FA220347375ac4f91f9E4A4AAb362F22801504",
        "num_coins": 2,
        "name": "xaut3crv",
        "base_pool": BASE_POOLS["tripool"]["pool"],
        "has_positive_rebasing_tokens": False,
    },
    "spelleth" : {
        "pool": "0x98638FAcf9a3865cd033F36548713183f6996122",
        "lp_token": "0x8282BD15dcA2EA2bDf24163E8f2781B30C43A2ef",
        "gauge": "0x08380a4999Be1a958E2abbA07968d703C7A3027C",
        "zap": ZERO_ADDRESS,
        "num_coins": 2,
        "name": "spelleth",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "teth" : {
        "pool": "0x752eBeb79963cf0732E9c0fec72a49FD1DEfAEAC",
        "lp_token": "0xCb08717451aaE9EF950a2524E33B6DCaBA60147B",
        "gauge": "0x6070fBD4E608ee5391189E7205d70cc4A274c017",
        "zap": ZERO_ADDRESS,
        "num_coins": 2,
        "name": "teth",
        "base_pool": ZERO_ADDRESS,
        "has_positive_rebasing_tokens": False,
    },
    "eurocusd" : {
        "pool": "0xE84f5b1582BA325fDf9cE6B0c1F087ccfC924e54",
        "lp_token": "0x70fc957eb90e37af82acdbd12675699797745f68",
        "gauge": "0x4329c8F09725c0e3b6884C1daB1771bcE17934F9",
        "zap": "0xd446a98f88e1d053d1f64986e3ed083bb1ab7e5a",
        "num_coins": 2,
        "name": "eurocusd",
        "base_pool": BASE_POOLS["tripool"]["pool"],
        "has_positive_rebasing_tokens": False,
    },
}


@click.group(short_help="Deploy the project")
def cli():
    pass

@cli.command(cls=NetworkBoundCommand)
@network_option()
@account_option()
def main(network, account):
    
    # deploy basepool registry:
    base_pool_registry = account.deploy(project.BasePoolRegistry)
    
    # populate base pool registry:
    for _, data in BASE_POOLS.items():
        base_pool_registry.add_base_pool(
            data["pool"],
            data["lp_token"],
            data["num_coins"],
            data["is_legacy"],
            data["is_lending"],
            data["is_v2"],
            sender=account,
        )
    
    crypto_registry = account.deploy(
        project.CryptoRegistryV1, ADDRESS_PROVIDER, base_pool_registry
    )
    
    # populate crypto registry:
    for _, pool in CRYPTO_REGISTRY_POOLS.items():
        crypto_registry.add_pool(
            pool["pool"],
            pool["lp_token"],
            pool["gauge"],
            pool["zap"],
            pool["num_coins"],
            pool["name"],
            pool["base_pool"],
            pool["has_positive_rebasing_tokens"],
            sender=account,
        )
    
    # deploy registry handlers:
    stable_registry_handler = account.deploy(
        project.StableRegistryHandler, STABLE_REGISTRY_ADDRESS
    )
    stable_factory_handler = account.deploy(
        project.StableFactoryHandler, 
        STABLE_REGISTRY_ADDRESS, 
        base_pool_registry
    )
    crypto_registry_handler = account.deploy(
        project.CryptoRegistryHandler, crypto_registry
    )
    crypto_factory_handler = account.deploy(
        project.CryptoFactoryHandler, 
        CRYPTO_FACTORY_ADDRESS, 
        base_pool_registry
    )
    
    # deploy metaregistry:
    metaregistry = account.deploy(
        project.MetaRegistry,
        ADDRESS_PROVIDER
    )
    
    # populate metaregistry:
    metaregistry.add_registry_handler(stable_registry_handler, sender=account)
    metaregistry.add_registry_handler(stable_factory_handler, sender=account)
    metaregistry.add_registry_handler(crypto_registry_handler, sender=account)
    metaregistry.add_registry_handler(crypto_factory_handler, sender=account)
