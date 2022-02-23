from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    # Getting accountn 0
    account = accounts[0]
    # Deploying the lottery contract.
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],{"from": account})
    # Checking
    assert lottery.getEntranceFee() > Web3.toWei(0.017,"ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.022,"ether")
