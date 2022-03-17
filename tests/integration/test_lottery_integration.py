# Integration Test: A Way of Testing Multiple Complex Systems. These test's are basically used to test on a Real TestNet such as Rinkeby etc.

import time
from brownie import Lottery, accounts, config, network
import pytest
from web3 import Web3
from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
     # Setting up variables.
    lottery = deploy_lottery()
    account = get_account(id="test_account")
    # Acting (Starting Lottery & Entering It)
    lottery.startLottery({"from": account})
    # Creating entries for the lottery.
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Funding the link.
    fund_with_link(lottery)
    # Calling End Lottery
    transaction = lottery.endLottery({"from": account})
    # This is real network. Here we dont need to pretend to be a Chainlink Node.
    # Just wait for the Chainlink Node to Respond.
    time.sleep(60)
    time.sleep(60)
    time.sleep(60)
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0