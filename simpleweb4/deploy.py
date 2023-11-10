from solcx import compile_standard, install_solc
import json
from decouple import config
from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv

with open("./simpleStorage.sol", "r") as file:
    _simpleStoragefile = file.read()
print("Installing...")
install_solc("0.6.0")
load_dotenv()
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": _simpleStoragefile}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)
abi = compiled_sol["contracts"]["simpleStorage.sol"]["simpleStorage"]["abi"]
bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["simpleStorage"]["evm"][
    "bytecode"
]["object"]

# connect to a local blockchain
w3 = Web3(Web3.HTTPProvider(config("GANACHE_URL")))
chainId = 1337
if chainId == 4:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
address = config("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# contract creation
simpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(address)

print("Deploying contract...")
tx = simpleStorage.constructor().build_transaction(
    {
        "chainId": chainId,
        "from": address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.toWei("20", "gwei"),
    }
)
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!...")

# contract call
_simpleStorage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial value:  {_simpleStorage.functions.retrieve().call()}")
print("Updating contract...")
tx = _simpleStorage.functions.store(1).build_transaction(
    {
        "chainId": chainId,
        "from": address,
        "nonce": nonce + 1,
        "gas": 2000000,
        "gasPrice": w3.toWei("20", "gwei"),
    }
)
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!...")
print("Updated value: ", _simpleStorage.functions.retrieve().call())
print("Updating contract...")
tx = _simpleStorage.functions.store(2).build_transaction(
    {
        "chainId": chainId,
        "from": address,
        "nonce": nonce + 2,
        "gas": 2000000,
        "gasPrice": w3.toWei("20", "gwei"),
    }
)
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!...")
print("Updated value: ", _simpleStorage.functions.retrieve().call())
print("Updating contract...")
tx = _simpleStorage.functions.store(3).build_transaction(
    {
        "chainId": chainId,
        "from": address,
        "nonce": nonce + 3,
        "gas": 2000000,
        "gasPrice": w3.toWei("20", "gwei"),
    }
)
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!...")
print(f"Updated value:  {_simpleStorage.functions.retrieve().call()}")
