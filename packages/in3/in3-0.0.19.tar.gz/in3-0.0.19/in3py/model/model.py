from typing import List, Mapping, Tuple
import enum
import json
from in3py.exceptions.in3_exceptions import IN3NumberFormatException, HashFormatException, AddressFormatException
from in3py.enums.in3 import EnumsBlockStatus

class In3Model:

    def to_dict(self):
        return ModelUtils.to_dict(self)


class RPCResponse:

    def __init__(self, id:str=None, jsonrpc:str=None, result:str=None, error=None):
        self.id = id
        self.jsonrpc = jsonrpc
        self.result=result
        self.error=None

    def __str__(self):
        return json.dumps(ModelUtils.to_dict(self))


class IN3NodeWeight(In3Model):

    def __init__(self):
        self.weight:int=None
        self.responseCount:int=None
        self.avgResponseTime:int=None
        self.pricePerRequest:int=None
        self.lastRequest:int=None
        self.blacklistedUntil:int=None


class IN3NodeConfig(In3Model):

    def __init__(self):
        self.index:int=None
        self.address:str=None
        self.timeout:int=None
        self.url:str=None
        self.chainIds:List[str]=None
        self.deposit:int=None
        self.capacity:int=None
        self.props:int=None


class ChainSpec(In3Model):

    def __init__(self):
        self.engine:str=None
        self.validatorContract:str=None
        self.validatorList:List=None


class IN3ConfigServer(In3Model):

    def __init__(self):
        self.verifier:str = None
        self.name:str = None
        self.chainSpec:ChainSpec = None


class Chain:

    def __init__(self, registry=None, chain_id=None, status=None, node_list=None, alias=None):
        self.registry = registry
        self.chain_id = chain_id
        self.status = status
        self.node_list = node_list
        self.alias = alias

    def value(self):
        return self.chain_id

@enum.unique
class EnumsChains(enum.Enum):

    MAINNET = Chain(registry="0x2736D225f85740f42D17987100dc8d58e9e16252",
                    chain_id="0x1",
                    alias="mainnet",
                    status="https://libs.slock.it?n=mainnet",
                    node_list="https://libs.slock.it/mainnet/nd-3")

    KOVAN = Chain(
                    registry= "0x27a37a1210df14f7e058393d026e2fb53b7cf8c1",
                    chain_id= "0x2a",
                    alias="kovan",
                    status= "https://libs.slock.it?n=kovan",
                    node_list= "https://libs.slock.it/kovan/nd-3")

    EVAN = Chain(
                    registry="0x85613723dB1Bc29f332A37EeF10b61F8a4225c7e",
                    chain_id="0x4b1",
                    alias="evan",
                    status="https://libs.slock.it?n=evan",
                    node_list="https://libs.slock.it/evan/nd-3")

    GOERLI = Chain(
                    registry="0x85613723dB1Bc29f332A37EeF10b61F8a4225c7e",
                    chain_id="0x5",
                    alias="goerli",
                    status="https://libs.slock.it?n=goerli",
                    node_list="https://libs.slock.it/goerli/nd-3")

    IPFS = Chain(
                    registry="0xf0fb87f4757c77ea3416afe87f36acaa0496c7e9",
                    chain_id="0x7d0",
                    alias="ipfs",
                    status="https://libs.slock.it?n=ipfs",
                    node_list="https://libs.slock.it/ipfs/nd-3")


class Address:

    def __init__(self, address:str):
        self.__value=self.__validate(address=address)

    def __str__(self):
        return self.__value

    def __validate(self,address:str):
        if address.startswith("0x"):
            address = address[2:]

        if len(address.encode("utf-8")) is not 40:
            raise AddressFormatException("The address don't have enough size as needed.")

        if ModelUtils.address_checksum(address, False) != address:
            raise AddressFormatException("The Address it's not in a correct checksum.")

        return "0x"+address



class Hash:

    def __init__(self, hash:str):
        self.__hash = self.__validate(hash=hash)

    def __str__(self):
        return self.__hash

    def __validate(self, hash:str):
        if hash.startswith("0x"):
            hash = hash[2:]
        if len(hash.encode("utf-8")) is not 64:
            raise HashFormatException

        return "0x"+hash


class IN3Number:

    def __init__(self, number):
        if isinstance(number,str):
            try:
                number = int(number, 16)
            except ValueError:
                raise IN3NumberFormatException()

        self.__number = number

    def to_hex(self) -> str:
        return hex(self.__number)

    def to_int(self) -> int:
        return self.__number

    def __str__(self):
        return self.to_hex()


class IN3Config(In3Model):

    def __init__(self):
        self.autoUpdateList:bool=None
        self.chainId:Chain=EnumsChains.MAINNET.value
        self.finality:int=None
        self.includeCode:bool=None
        self.keepIn3:bool=None
        self.key=None
        self.maxAttempts:int=None
        self.maxBlockCache:int=None
        self.maxCodeCache:int=None
        self.minDeposit:int=None
        self.nodeLimit:int=None
        self.proof:str=None
        self.replaceLatestBlock:int=None
        self.requestCount:int=None
        self.rpc:str=None
        self.servers:List[IN3ConfigServer]=None
        self.signatureCount:int=None
        self.verifiedHashes:List=None


class Transaction(In3Model):

    mapping = {
        "_from": Address,
        "to": Address,
        "gas":int,
        "gas_price": int,
        "value": int,
        "data":str,
        "nonce": int
    }

    def __init__(self, _from: Address, to: Address=None, gas:int=90000, gas_price:int=None , value: int=None, data:str=None, nonce:int=None ):
        self._from = _from
        self.to = to
        self.gas = gas
        self.gas_price = gas_price
        self.value  = value
        self.data = data
        self.nonce = nonce

    def __str__(self):
        return json.dumps(ModelUtils.to_dict(self))

    @staticmethod
    def from_json(json):
        t_aux = Transaction(_from=None)
        ModelUtils.from_json(json=json, mapping=Transaction.mapping, object_instance=t_aux)
        return t_aux


class Block(In3Model):

    def __init__(self, block_hash: Hash, block_number: IN3Number, _from:Address, gas: IN3Number,gas_price:IN3Number,  hash: Hash , input:str, nonce: IN3Number, to:Address, transaction_index: IN3Number, value: IN3Number ):
        self.block_hash = block_hash
        self.block_number = block_number
        self._from = _from
        self.gas = gas
        self.gas_price = gas_price
        self.hash = hash
        self.input = input
        self.nonce = nonce
        self.to = to
        self.transaction_index = transaction_index
        self.value = value


class RPCRequest:

    def __init__(self, jsonrpc: str = "2.0", method:enum.Enum= None , params: Tuple = None, id: int = 1):
        self.jsonrpc = jsonrpc
        self.method = method
        self.params = params
        self.id = id

    def __str__(self):
        return json.dumps(ModelUtils.to_dict(self))

    def to_utf8(self):
        return self.__str__().encode("utf-8")


class ModelUtils:

    @staticmethod
    def to_dict(clazz):
        aux = clazz.__dict__
        result = {}
        for i in aux:
            if aux[i] is None:
                continue

            arr = i.split("_")
            r = ""
            index_aux = 0
            for arr_aux in arr:
                if arr_aux is '':
                    continue
                r += arr_aux[index_aux].upper() + arr_aux[index_aux + 1:]
            key = r[0].lower() + r[1:]

            value = None
            if isinstance(aux[i],Tuple):
                value = []
                for a in aux[i]:
                    value.append(ModelUtils.get_val_from_object(a))
            else:
                value = ModelUtils.get_val_from_object(aux[i])

            result[key] = value

        return result

    @staticmethod
    def get_val_from_object(item):
        aux = item
        if isinstance(item, Chain):
            aux = item.value()
        if isinstance(item, enum.Enum):
            aux = item.value
        if isinstance(item, IN3Number):
            aux = item.to_hex()
        if isinstance(item, Address):
            aux = item.__str__()
        if isinstance(item, Hash):
            aux = item.__str__()
        if isinstance(item, In3Model):
            aux = item.to_dict()

        return aux


    @staticmethod
    def address_checksum(address: str, prefix:bool=True):
        from in3py.ethereum.ethereum import Ethereum

        checked = ""
        address = address.lower()

        if address.startswith("0x"):
            address = address[2:]

        sha3_aux = Ethereum().web3_sha3(address).result[2:]

        for i_addr, i_sha in zip(list(address), list(sha3_aux)):
            if int(i_sha, 16) >= 8:
                i_addr = str(i_addr).upper()

            checked += i_addr

        if prefix:
            return "0x" + checked
        return checked

    @staticmethod
    def camel_case_name_of(name):
        aux = name.split("_")
        result="";
        for a in aux:
            if a is "":
                continue
            result+=a[0].upper()+a[1:]
        return result[0].lower()+result[1:]


    @staticmethod
    def from_json(json, mapping, object_instance):
        result = {}
        for m in mapping:
            name = ModelUtils.camel_case_name_of(m)
            try:
                result[m] = mapping[m](json[name])
            except:
                pass

        object_instance.__dict__.update(result)
        return object_instance


class TransactionReceipt(In3Model):

    def __init__(self,
                 transaction_hash: Hash,
                 transaction_index: IN3Number,
                 block_hash: Hash,
                 block_number:IN3Number,
                 _from:Address,
                 to:Address,
                 cumulative_gas_used:IN3Number,
                 gas_used:IN3Number,
                 contract_address:IN3Number,
                 logs: List,
                 logs_bloom: str
                 ):
        self.transaction_hash = transaction_hash
        self.transaction_index = transaction_index
        self.block_hash= block_hash
        self.block_number=block_number
        self._from = _from
        self.to = to
        self.cumulative_gas_used = cumulative_gas_used
        self.gas_used = gas_used
        self.contract_address = contract_address
        self.logs = logs
        self.logs_bloom = logs_bloom


class Filter(In3Model):

    def __init__(self, fromBlock:[IN3Number, EnumsBlockStatus]=None, toBlock:[IN3Number,  EnumsBlockStatus]=None, address:Address=None, topics:List=None, blockhash:Hash=None):
        self.fromBlock=  fromBlock
        self.toBlock =toBlock
        self.address= address
        self.topics= topics
        self.blockhash=blockhash


class Logs(In3Model):

    def __init__(self,
                 log_index:IN3Number,
                 transaction_index:IN3Number,
                 transaction_hash:Hash,
                 block_hash:Hash,
                 block_number:IN3Number,
                 address:Address,
                 data:str,
                 topics:List):

        self.log_index =log_index
        self.transaction_index = transaction_index
        self.transaction_hash =transaction_hash
        self.block_hash = block_hash
        self.block_number = block_number
        self.address =address
        self.data= data
        self.topics =topics

