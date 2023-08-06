from in3py.runner.in3_runner import In3Runner
from in3py.model.model import RPCRequest,Address,  IN3Number, Hash, Transaction, Filter
from in3py.enums.in3 import EnumsEthCall
from in3py.enums.in3 import EnumsBlockStatus


class Ethereum:

    def web3_sha3(self, data:str):
        rpc = RPCRequest(method=EnumsEthCall.WEB3_SHA3, params=(data,))
        return In3Runner.call_in3_rpc(rpc)

    def get_balance(self, address: Address):
        rpc = RPCRequest(method=EnumsEthCall.ACCOUNTS, params=(address, ))
        return In3Runner.call_in3_rpc(rpc)

    def gas_price(self):
        rpc = RPCRequest(method=EnumsEthCall.GAS_PRICE)
        return In3Runner.call_in3_rpc(request=rpc)

    def accounts(self):
        rpc = RPCRequest(method=EnumsEthCall.ACCOUNTS)
        return In3Runner.call_in3_rpc(request=rpc)

    def block_number(self):
        rpc = RPCRequest(method=EnumsEthCall.BLOCK_NUMBER)
        return In3Runner.call_in3_rpc(request=rpc)

    def get_balance(self, address:Address, number:[EnumsBlockStatus,IN3Number]=EnumsBlockStatus.LATEST):
        rpc = RPCRequest(method=EnumsEthCall.BALANCE, params=(address,number, ))
        return In3Runner.call_in3_rpc(request=rpc)

    def  get_storage_at(self, address:Address, position:IN3Number , number:[EnumsBlockStatus, IN3Number ]):
        rpc = RPCRequest(method=EnumsEthCall.STORAGE_AT, params=(address,position,number,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_transaction_count(self, address:Address, number:[IN3Number,EnumsBlockStatus]):
        rpc = RPCRequest(method=EnumsEthCall.TRANSACTION_COUNT, params=(address,number,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_block_transaction_count_by_hash(self, block_hash: Hash ):
        rpc = RPCRequest(method=EnumsEthCall.BLOCK_TRANSACTION_COUNT_BY_HASH, params=(block_hash,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_block_transaction_count_by_number(self, number: [IN3Number,EnumsBlockStatus] ):
        rpc = RPCRequest(method=EnumsEthCall.BLOCK_TRANSACTION_COUNT_BY_NUMBER, params=(number,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_uncle_count_by_block_hash(self, block_hash:Hash):
        rpc = RPCRequest(method=EnumsEthCall.UNCLE_COUNT_BY_BLOCK_HASH, params=(block_hash,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_uncle_count_by_block_number(self, number:[IN3Number,EnumsBlockStatus]):
        rpc = RPCRequest(method=EnumsEthCall.UNCLE_COUNT_BY_BLOCK_NUMBER, params=(number,))
        return In3Runner.call_in3_rpc(request=rpc)

    def get_code(self, address:Address, number:[IN3Number,  EnumsBlockStatus ]):
        rpc =RPCRequest(method=EnumsEthCall.CODE,  params=(address,number,) )
        return In3Runner.call_in3_rpc(request=rpc)

    def sign(self, address:Address, message:str):
        rpc = RPCRequest(method=EnumsEthCall.SIGN, params=(address, message,))
        return In3Runner.call_in3_rpc(request=rpc)

    def send_transaction(self, transaction:Transaction):
        rpc = RPCRequest(method=EnumsEthCall.SEND_TRANSACTION, params=(transaction,))
        return In3Runner.call_in3_rpc(request=rpc)

    def send_raw_transaction(self, data:str):
        rpc = RPCRequest(method=EnumsEthCall.SEND_RAW_TRANSACTION, params=(data,))
        return In3Runner.call_in3_rpc(request=rpc)

    def call(self, transaction:Transaction):
        rpc = RPCRequest(method=EnumsEthCall.CALL, params=(transaction,))
        return In3Runner.call_in3_rpc(rpc)

    def estimate_gas(self, transaction:Transaction):
        rpc = RPCRequest(method=EnumsEthCall.ESTIMATE_TRANSACTION, params=(transaction,))
        return In3Runner.call_in3_rpc(rpc)

    def get_block_by_hash(self, hash:Hash, is_full:bool=True):
        rpc = RPCRequest(method=EnumsEthCall.BLOCK_BY_HASH,params=(hash,is_full,))
        return In3Runner.call_in3_rpc(rpc)

    def get_block_by_number(self, number:[IN3Number, EnumsBlockStatus, str], is_full:bool=True):
        rpc = RPCRequest(method=EnumsEthCall.BLOCK_BY_NUMBER,params=(number,is_full,))
        return In3Runner.call_in3_rpc(rpc)

    def get_transaction_by_hash(self, hash:Hash):
        rpc = RPCRequest(method=EnumsEthCall.TRANSACTION_BY_HASH, params=(hash,))
        return In3Runner.call_in3_rpc(rpc)

    def get_transaction_by_block_hash_and_index(self,block_hash:Hash,index:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.TRANSACTION_BY_BLOCKHASH_AND_INDEX, params=(block_hash,index,))
        return  In3Runner.call_in3_rpc(rpc)

    def get_transaction_by_block_number_and_index(self, block_number:[IN3Number, EnumsBlockStatus], index:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.TRANSACTION_BY_BLOCKNUMBER_AND_INDEX,params=(block_number,index,))
        return In3Runner.call_in3_rpc(rpc)

    def get_transaction_receipt(self, hash: Hash):
        rpc = RPCRequest(method=EnumsEthCall.TRANSACTION_RECEIPT, params=(hash,))
        return In3Runner.call_in3_rpc(rpc)

    def pending_transactions(self):
        rpc = RPCRequest(method=EnumsEthCall.PENDING_TRANSACTIONS)
        return In3Runner.call_in3_rpc(rpc)

    def get_uncle_by_block_hash_and_index(self, block_hash:Hash, index:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.UNCLE_BY_BLOCKHASH_AND_INDEX, params=(block_hash,index,))
        return In3Runner.call_in3_rpc(rpc)

    def get_uncle_by_block_number_and_index(self, block_number:IN3Number, index:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.UNCLE_BY_BLOCKHASH_AND_INDEX, params=(block_number,index,))
        return In3Runner.call_in3_rpc(rpc)

    def new_filter(self, filter:Filter):
        rpc = RPCRequest(method=EnumsEthCall.NEW_FILTER, params=(filter, ))
        return In3Runner.call_in3_rpc(rpc)

    def new_block_filter(self):
        rpc=  RPCRequest(method=EnumsEthCall.NEW_BLOCK_FILTER)
        return In3Runner.call_in3_rpc(rpc)

    def new_pending_transaction_filter(self):
        rpc= RPCRequest(method=EnumsEthCall.NEW_PENDING_TRANSACTION_FILTER)
        return In3Runner.call_in3_rpc(rpc)

    def uninstall_filter(self, filter_id:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.UNINSTALL_FILTER, params=(filter_id,))
        return In3Runner.call_in3_rpc(rpc)

    def get_filter_changes(self, filter_id:IN3Number):
        rpc = RPCRequest(method=EnumsEthCall.FILTER_CHANGES,params=(filter_id,) )
        return In3Runner.call_in3_rpc(rpc)

    def get_filter_logs(self, filter_id:IN3Number):
        rpc =RPCRequest(method=EnumsEthCall.FILTER_LOGS, params=(filter_id,))
        return In3Runner.call_in3_rpc(rpc)

    def get_logs(self, filter:Filter):
        rpc =RPCRequest(method=EnumsEthCall.LOGS, params=(filter,))
        return In3Runner.call_in3_rpc(rpc)
























