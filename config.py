from web3 import Web3
import json

# Web3 / Ganache Setup
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
with open('build/TouristIDRegistry.abi') as f:
    contract_abi = json.load(f)

contract_address = '0xA7598ED10DA4e016Ad520dD95F8677a4fAe84c70'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)
