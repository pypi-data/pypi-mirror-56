## IN3 Python Client

This is a simple test using in3 python library

### Creating a new instance 
```
in3 = In3Client()
```

### Creating a new instance from default configurations
```
In3Client.create_in3_client_from_default_config()
```

### Creating a new instance from my custom configuration
```
config = IN3Config()
config.chainId = EnumsChains.MAINNET.value.chain_id
in3 = In3Client(config=config)
```

### Calling ETH function from our In3 Client

```
in3  = In3Client.create_in3_client_from_default_config()
in3.eth.block_number()
```

## In3Types

We have some classes that can help you write some simple and safe codes using our client.

### Bytes20
This class help you write 20 bytes parameters and validate it
```python
from src.domain.bytes_types import Bytes20
address = Bytes20('0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b')
```

### Bytes32
This class help you write 32 bytes paramters like hashes.
```python
from src.domain.bytes_types import Bytes32
block_hash = Bytes32('0xc94770007dda54cF92009BFF0dE90c06F603a09f')
```

### In3Number
This class can help you write numbers (hex and int) to handle block numbers

```python
from src.domain.in3_number import In3Number
number = In3Number(0x76c0)
number.to_hex() #0x76c0
number.to_int() #30400

```

### EnumBlockStatus

This Enum stands for block number parameters string "latest", "earliest" or "pending"

```python
from src.enums.enums_block_status import EnumsBlockStatus
default_block_number = EnumsBlockStatus.LATEST

```

## Functions

We can call different kinds of functions using the In3 Client.

##### *IPFS will be supported soon


### Ethereum

You can call ethereum functions using our client

* Assuming that you have the In3 Client setted correctly as we did before, we can call these functions.


```
in3 = In3Client.create_in3_client_from_default_config()
in3.eth
```


The eth module is responsible to call all ethereum functions using our client to make the things easier.


#### [gas_price](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_gasprice)

Returns the current price per gas in wei.


```python
in3.eth.gas_price()

```


#### [accounts](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_accounts)

Return all accounts

```python
in3.eth.accounts()

```


#### [block_number](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_blockNumber)

Returns the number of most recent block.


```python
in3.eth.block_number()

```

#### [get_balance](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getBalance)

Returns the balance of the account of given address.

```python
address = '0xc94770007dda54cF92009BFF0dE90c06F603a09f'
in3.eth.get_balance(address, EnumsBlockStatus.LATEST)
```

#### [getTransactionCount](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getTransactionCount)
Returns the number of transactions sent from an address.

```python
from src.domain.bytes_types import Bytes20
address = Bytes20('0xc94770007dda54cF92009BFF0dE90c06F603a09f')
number  = eth.get_transaction_count(address,EnumsBlockStatus.LATEST)
```

#### [send_transaction](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendTransaction)
Creates new message call transaction or a contract creation, if the data field contains code.
```python
from src.dto.transaction_dto import TransactionDTO

transactionDTO = TransactionDTO(From="0xb60e8dd61c5d32be8058bb8eb970870f07233155",
                                to="0xd46e8dd67c5d32be8058bb8eb970870f07244567",
                                data="0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675",
                                gas="0x76c0",
                                gasPrice="0x9184e72a000",
                                value="0x9184e72a"
                                )
eth.send_transaction(transactionDTO)
```

#### [get_block_by_hash](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getBlockByHash)
Returns information about a block by hash.

```python
from src.domain.bytes_types import Bytes32
hash = Bytes32('0xdcded60b27fc1fc3987e9416cb3dd81159552426ab6e027a308ea94985a7f258')
eth.get_block_by_hash(hash,False)
```

#### [get_block_by_number](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getBlockByNumber)
Returns information about a block by block number.

```python
from src.domain.in3_number import In3Number

num = In3Number(0x6a5c56)
eth.get_block_by_number(num, full=False)
```

#### [get_transaction_by_hash](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getTransactionByHash)

Returns information about a transaction by block hash and transaction index position.

```python
eth =  self.get_in3_core()
address = Bytes32('0x88df016429689c079f3b2f6ad39fa052532c56795b733da78a91ebe6a713944b')
eth.get_transaction_by_hash(address)
```

### [eth_getTransactionByBlockHashAndIndex](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getTransactionByBlockHashAndIndex)

Returns information about a transaction by block hash and transaction index position.

```python
block_hash = Bytes32('0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331')
num = In3Number(0x0)
eth.get_transaction_by_block_hash_and_index(block_hash, num)

```

### [eth_getTransactionByBlockNumberAndIndex](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getTransactionByBlockNumberAndIndex)

Returns information about a transaction by block number and transaction index position.

```python
number = In3Number(0x29c)
index = In3Number(0x0)
eth.get_transaction_by_block_number_and_index(number, index)

```

#### [get_transaction_receipt](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getTransactionReceipt)

Returns the receipt of a transaction by transaction hash.

```python
eth.get_transaction_receipt(Bytes32('0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238'))

```

#### [pending_transactions](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_pendingTransactions)
Returns the pending transactions list.

```python
eth.pending_transactions()
```
#### [eth_getUncleByBlockHashAndIndex](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getUncleByBlockHashAndIndex)
Returns information about a uncle of a block by hash and uncle index position.

```python
hash = Bytes32('0xc6ef2fc5426d6ad6fd9e2a26abeab0aa2411b7ab17f30a99d3cb96aed1d1055b')
index= In3Number(0x0)
number = eth.get_uncle_by_block_hash_and_index(hash, index)
```
#### [get_uncle_by_block_number_and_index](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getUncleByBlockNumberAndIndex)
Returns information about a uncle of a block by number and uncle index position.

```python
number = In3Number(0x29c)
index = In3Number(0x0)
eth.get_uncle_by_block_number_and_index(number, index)
```

#### [eth_sendRawTransaction](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sendRawTransaction)
TODO
#### [eth_call](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_call)
TODO
#### [eth_estimateGas](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_estimateGas)
TODO

#### [eth_getBlockTransactionCountByHash](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getBlockTransactionCountByHash)
Returns the number of transactions in a block from a block matching the given block hash.

```python
Bytes32('0xb903239f8543d04b5dc1ba6579132b143087c68db1b2168786408fcbce568238')
eth.get_block_transaction_count_by_hash(hash)
```

#### [eth_getBlockTransactionCountByNumber](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getBlockTransactionCountByNumber)
Returns the number of transactions in a block matching the given block number.

```python
eth.get_block_transaction_count_by_number(EnumsBlockStatus.LATEST)
```

#### [eth_getUncleCountByBlockHash](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getUncleCountByBlockHash)
Returns the number of uncles in a block from a block matching the given block hash.

```python
hash = Bytes32('0xc94770007dda54cF92009BFF0dE90c06F603a09f')
eth.get_uncle_count_by_block_hash(hash)
```

#### [eth_getUncleCountByBlockNumber](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getUncleCountByBlockNumber)
Returns the number of uncles in a block from a block matching the given block number.

```python
eth.get_uncle_count_by_block_number(EnumsBlockStatus.LATEST)
```

#### [eth_sign](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_sign)
The sign method calculates an Ethereum specific signature with: sign(keccak256("\x19Ethereum Signed Message:\n" + len(message) + message))).

By adding a prefix to the message makes the calculated signature recognisable as an Ethereum specific signature. This prevents misuse where a malicious DApp can sign arbitrary data (e.g. transaction) and use the signature to impersonate the victim.

Note the address to sign with must be unlocked.

```python
address = Bytes20('0x9b2055d370f73ec7d8a03e965129118dc8f5bf83')
message = '0xdeadbeaf'
eth.sign(address,message)
```

#### [get_storage_at](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getStorageAt)
Returns the value from a storage position at a given address.

```python
address = Bytes20('0x295a70b2de5e3953354a6a8344e616ed314d7251')
position = In3Number(0x0)
storage = eth.get_storage_at(address, position, EnumsBlockStatus.LATEST)
```
#### [get_code](https://github.com/ethereum/wiki/wiki/JSON-RPC#eth_getCode)

```python
address = Bytes20('0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b')
number = In3Number(0x0)
code = eth.get_code(address, number)
```