// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import '@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol';
import '@chainlink/contracts/src/v0.8/VRFConsumerBase.sol';
import "@openzeppelin/contracts/access/Ownable.sol";

abstract contract Lottery is VRFConsumerBase, Ownable{

    address payable[] public players;
    uint256 public usdEntryFee;
    uint256 public randomness;
    AggregatorV3Interface internal ethUSDPriceFeed;
    address payable public recentWinner;

    // Enum is basically setting some specific values to a varible. (1st is 0, 2nd is 1..and so on)
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;

    // KeyHash is a way to uniquely identify VRFNode.
    //
    constructor(address _priceFeed, address _vrfCoordinator, address _link, uint256 f, bytes32 keyhash) VRFConsumerBase(_vrfCoordinator, _link) {
        // Setting lottery state to closed.
        lottery_state = LOTTERY_STATE.CLOSED;
        
        // Setting entry fee in wei.
        usdEntryFee = 50 * 10 ** 18;
        // Getting the latest price.
        ethUSDPriceFeed = AggregatorV3Interface(_priceFeed);
        fee = f;
        keyHash = keyhash;
    }

    function enter() public payable {
        // 50$ minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "The minimum required is 50$");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns(uint256) {
        (,int answer,,,) = ethUSDPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(answer) * 10 ** 10; //Adding 10 more Decimals to already existing 8 Deciamals. Hence 18 Decimals.
        uint256 costToEnter = (usdEntryFee * 10 ** 18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "[Lottery] Can't Start a New Lottery.");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash,fee);
    }

    function fullfillRandomness(bytes32 _requestId, uint256 _randomness) internal { 
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "You are'nt there yet!");
        require(_randomness > 0, "Random Not Found!");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        payable(recentWinner).transfer(address(this).balance);

        //Resetting
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
     }
}