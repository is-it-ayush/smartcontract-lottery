from brownie import network,config, Lottery
from .helpful_scripts import get_account,getContract

def deploy_lottery():
    account = get_account(index=0)
    lottery = Lottery.deploy(
        getContract("eth_usd_price_feed").address, 
        getContract("vrf_coordinator").address,
        getContract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"], 
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )

    print(f'[Contract] Lottery Contract has been deployed at {lottery.address}')

def main():
    deploy_lottery()

# Returns priceFeed depending upon the network.
