from in3py.model.model import RPCRequest, RPCResponse, IN3Number
from in3py.enums.in3 import EnumsEthCall
from in3py.runner.shared_library_runner import in3_create
from in3py.runner.shared_library_runner import in3_free
from in3py.runner.shared_library_runner import in3_exec
import json


class _In3Shared:

    def __init__(self):
        self.in3  = in3_create()

    def call(self, rpc):
        return in3_exec(self.in3, rpc)

    def release(self):
        in3_free(self.in3)


class In3Runner:

    __INSTANCE = None

    @staticmethod
    def get_instance():
        if In3Runner.__INSTANCE is None:
            In3Runner.__INSTANCE = _In3Shared()
        return In3Runner.__INSTANCE

    @staticmethod
    def call_in3_rpc(request: RPCRequest):
        response = In3Runner.get_instance().call(rpc=request.to_utf8())
        response_dict = json.loads(response.decode("utf-8").replace("\n"," "))
        rpc_response = RPCResponse()
        rpc_response.__dict__.update(response_dict)
        return In3Runner.__decode_result(rpc_response=rpc_response, method=request.method)

    @staticmethod
    def __decode_result(rpc_response:RPCResponse, method:EnumsEthCall):
        try:
            rpc_response.result = json.loads(rpc_response.result)
        except:
            pass

        return rpc_response






# rpc=  RPCRequest()
# rpc.method = EnumsEthCall.BLOCK_NUMBER
#
# r = In3Runner.call_in3_rpc(rpc)
# print(r)