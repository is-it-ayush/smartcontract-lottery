# Unit Test: These test's are basically used to test on a Development Environment. They are used to test snippets of code.
# Important: Test each & every line of code. 

from brownie import Lottery, accounts, config, network, exceptions
import pytest
from web3 import Web3
from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Deploying the lottery contract.
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    print(f"[Debug] Entrace Fee is {entrance_fee}")
    # Checking
    assert entrance_fee == Web3.toWei(0.025,"ether")

def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Setting Up Variables.
    lottery = deploy_lottery()
    # This will try to enter a lottery that hasnt started yet because we have't called lottery.startLottery() yet.
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), "value": lottery.getEntranceFee()})

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Setting up variables.
    lottery = deploy_lottery()
    account = get_account()
    # Acting (Starting Lottery & Entering It)
    lottery.startLottery({"from":account})
    lottery.enterLottery({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account