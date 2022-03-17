
from brownie import accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, network, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork","mainent-fork-dev"]
CONTRACT_TO_MOCK = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}
DECIMALS = 8
INITIAL_VALUE = 200000000000

# get_account(index=2): if index is provied, it will return an address from accounts[2]
# get_account(id="test_account"): if id is provided, it will load id from (real-life-accounts)
def get_account(index=None, id="test_account"):
    if index or network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[index]
    if id or network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts.load(id)
    return accounts[0]

# Getting the contract
def getContract(contractName):
    """ This function will grab the contract addresses from the bronwie config if defined, otherwise, it will dpeloy a mock version of the contract, and reuturn the address of mock contract.

        Args:
            contract_name(string)
        
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract.
    """
    # Getting which contract is the variable referring to.
    contract_type = CONTRACT_TO_MOCK[contractName] 
    # If network is not a real network i.e. a Local Blockchain Environment, deploy a mock so we can fetch the variable.
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # If the mock is already deployed, get the latest deployed mock else deploy one.
        if len(contract_type) <=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        # If this is a real netwrok, fetch the variable from brownie-config.yaml where its defined under networks section.
        contract_address = config["networks"][network.show_active()][contractName]
        # Then Get the details of contract from name, its address and its abi to interact with it.
        contract = Contract.from_abi(contract_type._name, contract_address , contract_type.abi)
    # Finally return the contract.
    return contract

# deploy_mocks(): To deploy the mocks. Take's Decimals and intital value.
def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    # Grab Account depending upon network.
    account = get_account()
    # Deploy a MockV3Agggregator from the values to get the price.
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    # Deploy LinkToken Mock to send $LINK to Randomess Generator.
    link_token = LinkToken.deploy({"from":account})
    # Deploy VRFCoordinator Mock to conenct with VRF Node.
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print(f"[Contract] The contract has been deployed.")


# fund_with_link(): This funds the latest deployed link_token contract with $LINK for Randomness to function.
def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): # 0.1 Link, which is the base fees or 10^17 Wei.
    account = account if account else get_account()
    link_token = link_token if link_token else getContract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from":account})
    tx.wait(1)
    print("[Contract] RandomNumberContract has been funded!")
    return tx


