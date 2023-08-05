# ocean-keeper
Wraps keeper contracts and web3 functions.

##### How to
The main class is `Keeper` and all contracts are accessible directly from the `keeper` instance.
Each deployed contract has a python wrapper class exposing the main functions and validating 
inputs.

```python
import os
from ocean_keeper import Keeper
from ocean_keeper.contract_handler import ContractHandler
from ocean_keeper.web3_provider import Web3Provider
from ocean_keeper.utils import get_account

# Init the web3 instance
Web3Provider.init_web3('http://localhost:8545')  # Assume running with local parity node
# set the contract handler path to abi files
ContractHandler.set_artifacts_path(os.path.expanduser('~/.ocean/keeper-contracts/artifacts'))
# get keeper instance
keeper = Keeper.get_instance(artifacts_path=ContractHandler.artifacts_path)
# Do stuff with keeper and it's contracts
account = get_account(0)
keeper.did_registry.register('0x10101010101010101010', '', 'http://localhost:5000/api/v1/assets', account)

```

Account can be specified using the following environment variables:
* PARITY_ADDRESS: the ethereum address
* PARITY_PASSWORD: the password to decrypt key in the `PARITY_ENCRYPTED_KEY`
* PARITY_KEY: the private key of this account (matches the `PARITY_ADDRESS`)
* PARITY_ENCRYPTED_KEY: the encrypted key in a json str
* PARITY_KEYFILE: path to the json file that has the encrypted key specified in json document

Note: The keys are loaded in this order: `PARITY_KEY`, `PARITY_ENCRYPTED_KEY`, `PARITY_KEYFILE`. If `PARITY_KEY` is 
specified the password and other environment variables are ignored.