# [Part-II] Brownie Framework SmartContract Lottery
This is the third part of working and understanding the working of Brownie. This is built following the tutorial by Patrick Collins on FreeCodeCamp with a touch of my own programming. I have also explained almost each line of Code in Comments.

# Objectives
- Users can enter the smart contract lottery based on a set fee. (Entrance Fee)
- An Admin (isn't decentralized anymore) will choose when the lottery is over.
- The lottery will select a random winner.

# Some Useful Commands
- ```brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=your_fork_url_will_go_here accounts=10 mnemonic=brownie port=8545```
This will add a network with your own fork url with the name of "mainnet-fork".  

- ```brownie networks delete mainnet-fork```
This will delete the netwrok mainnet-fork

# Resources
Here are the resources used to build and refrence the above made deploy.py file.
- [FreeCodeCamp Video By Patrick Collins](https://www.youtube.com/watch?v=M576WGiDBdQ&t=20988s&ab_channel=freeCodeCamp.org)
- [Patrick's GitHub Refrence](https://github.com/PatrickAlphaC/brownie_fund_me)
