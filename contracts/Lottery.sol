// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol';


contract Lottery {

    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUSDPriceFeed;

    constructor(address _priceFeed) public {
        usdEntryFee = 50 * 10 ** 18;
        ethUSDPriceFeed = AggregatorV3Interface(_priceFeed);
    }

    function enter() public payable {
        // 50$ minimum
        // require();
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {

    }

    function startLottery() public {

    }

    function endLottery() public {

    }
}