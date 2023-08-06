from in3py.model.in3_model import RPCRequest, RPCResponse
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
        # rpc_response.result = get_result_as_type(request.method, rpc_response.result)
        return get_result_as_type(request.method, rpc_response.result)


def get_result_as_type(method:EnumsEthCall, result:str):
    if method in [ EnumsEthCall.BALANCE, EnumsEthCall.GAS_PRICE, EnumsEthCall.BLOCK_NUMBER ]:
        return get_as_number(result)

    return result


def get_as_number(result:str):
    from in3py.model.in3_model import IN3Number
    return IN3Number(result)

# rpc=  RPCRequest()
# rpc.method = EnumsEthCall.BLOCK_NUMBER
#
# r = In3Runner.call_in3_rpc(rpc)
# print(r)