from brownie import accounts, network,config, Lottery
from .helpful_scripts import get_account,getContract,fund_with_link
import time

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

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from":account})
    starting_tx.wait(1)
    print("[Lottery] Lottery Has Been Started!")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000
    tx = lottery.enter({"from":account, "value":value})
    tx.wait(1)
    print(f"[Lottery] You enterted the lotter with value {value}")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Fund the contract
    tx = fund_with_link(lottery.address)
    tx.wait()
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"[]")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()

# Returns priceFeed depending upon the network.
