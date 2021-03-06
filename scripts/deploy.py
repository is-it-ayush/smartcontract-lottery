# Required Imports
from brownie import accounts, network,config, Lottery
from .helpful_scripts import get_account,getContract,fund_with_link
import time

# Function to deploy lottery contract.
def deploy_lottery():
    # This is ("""jhon doe""") used to sepcify the help() text for the function. Calling help(deploy_lottery) will fetch you the below text. 
    """Deploy's the Lottery Contract."""
    # Getting the account. Arguement Explaination explained in helpful_scripts.py file.
    account = get_account()
    # Deploying the Lottery Contract & assigning it to lottery variable.
    lottery = Lottery.deploy(
        # The arguemnt data is transferred to Lottery.sol contructor. We can specify & pass required data from python to solidity via this.
        getContract("eth_usd_price_feed").address, 
        getContract("vrf_coordinator").address,
        getContract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        # Every deployment will have this.
        {"from": account},
        # We fetch if we want to publish the contract depending upon network via brownie-config.yaml
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    # A little Update on Console.
    print(f'[Contract] Lottery Contract has been deployed at {lottery.address}')
    return lottery

def start_lottery():
    """Starts the Lottery."""
    # Getting Account as usual.
    account = get_account()
    # Getting the latest deployed Lottery.
    lottery = Lottery[-1]
    # Calling the SmartLottery Function in the contract.
    starting_tx = lottery.startLottery({"from":account})
    starting_tx.wait(1)
    # A little Console Update.
    print("[Lottery] Lottery Has Been Started!")

def enter_lottery():
    """Enter the lottery."""
    # Getting the account.
    account = get_account()
    # Getting latest deployed Lottery.
    lottery = Lottery[-1]
    # Getting the entrance fee and adding a few more to be on safer side for transaction process.
    value = lottery.getEntranceFee() + 100000
    # Entering the lottery with a amount. (Must be greater than 50$)
    tx = lottery.enter({"from":account, "value":value})
    tx.wait(1)
    # A little Console Update.
    print(f"[Lottery] You enterted the lotter with value {value}")

def end_lottery():
    """End's the lottery. Selects a Random Winner and initiates a transaction.
    \n time.sleep(180):\t This takes 3 minutes to be work due to on a real network it takes a huge amount of time for VRFCoordinatorNode to respond hence to prevent it from failing. Might implement a better way to do it later. """
    # Getting the account.
    account = get_account()
    # Getting the latest deployed Lottery.
    lottery = Lottery[-1]
    # Funding the Link Contract with $LINK (After deploying it). So we can get a random number from requestRandomness() function via Chainlink's "VRFConsumerBase.sol" Contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    # Calling endLottery() in our Lottery.sol Contract
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    # Declaring the winner.
    # Note: This wont return anything in Development Chain because "VRFCoordinator" will never call fullfillRandomness in Lottery.sol because there is no Chainlink Node on our Development Network to call VRFCoordinator which inturn would call fullfillRandomness.
    print(f"[Result] The Winner is: {lottery.recentWinner()}")

# Our Main Function.
def main():
    """This is the main function."""
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

# Returns priceFeed depending upon the network.
