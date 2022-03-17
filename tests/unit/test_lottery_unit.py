# Unit Test: These test's are basically used to test on a Development Environment. They are used to test snippets of code.
# Important: Test each & every line of code. 

from brownie import Lottery, accounts, config, network, exceptions
import pytest
from web3 import Web3
from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, getContract

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
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Setting up variables.
    lottery = deploy_lottery()
    account = get_account()
    # Acting (Starting Lottery & Entering It)
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    # Assert
    assert lottery.lottery_state() == 2

def test_can_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Setting up variables.
    lottery = deploy_lottery()
    account = get_account()
    # Acting (Starting Lottery & Entering It)
    lottery.startLottery({"from":account})
    # Creating entries for the lottery.
    for i in range(0,9):
        lottery.enter({"from":get_account(index=i), "value": lottery.getEntranceFee()})
    # Funding the link.
    fund_with_link(lottery)
    # Calling End Lottery
    transaction = lottery.endLottery({"from": account})
    # Getting the request Id to mock a random generation.
    request_id = transaction.events["RequestedRandomness"]["requestID"]
    # A Random Number to mock call VRFConsumerBase from VRFCoordinator.
    STATIC_RNG = 999
    # Calling the contract.
    getContract("vrf_coordinator").callBackWithRandomness(request_id,STATIC_RNG, lottery.address, {"from":account})
    # Getting Initial Variables to assert Later.
    inital_balance_of_accoount = account.balance()
    balance_of_lottery = lottery.balance()
    # Asserting
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == inital_balance_of_accoount + balance_of_lottery