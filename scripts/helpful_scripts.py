
from brownie import accounts, config, MockV3Aggregator, VRFCoordinatorMock, LinkToken, network, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development","ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork","mainent-fork-dev"]
CONTRACT_TO_MOCK = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken}
DECIMALS = 8
INITIAL_VALUE = 200000000000

# get_account(index=2): if index is provied, it will return an address from accounts[2]
# get_account(id="test_account"): if id is provided, it will load id from (real-life-accounts)
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
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
    contract_type = CONTRACT_TO_MOCK[contractName]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <=0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contractName]
        contract = Contract.from_abi(contract_type._name, contract_address , contract_type.abi)
    return contract

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print(f"[Contract] The contract has been deployed.")