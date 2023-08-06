from in3py.model.model import IN3Config
from in3py.model.model import RPCRequest
from in3py.enums.in3 import EnumIn3Methods
from in3py.runner.in3_runner import In3Runner
from in3py.model.model import EnumsChains,Address
from typing import List


class IN3:

    def config(self, in3_config):
        rpc = RPCRequest()
        rpc.params = (in3_config,)
        rpc.method = EnumIn3Methods.CONFIG
        return In3Runner.call_in3_rpc(rpc)

    def checksum_address(self, address:Address, chain: bool):
        rpc = RPCRequest()
        rpc.method=EnumIn3Methods.CHECKSUM_ADDRESS
        rpc.params=(address,chain,)
        return In3Runner.call_in3_rpc(rpc)

    def abi_encode(self, method:str, args:list):
        rpc = RPCRequest()
        rpc.method=EnumIn3Methods.ABI_ENCODE
        rpc.params=(method,args,)
        return In3Runner.call_in3_rpc(rpc)

    def abi_decode(self, signature:str, data:str):
        rpc = RPCRequest()
        rpc.method=EnumIn3Methods.ABI_DECODE
        rpc.params=(signature,data,)
        return In3Runner.call_in3_rpc(rpc)





