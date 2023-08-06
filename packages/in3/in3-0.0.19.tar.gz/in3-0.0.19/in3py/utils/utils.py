import json

from in3py.model.model import RPCRequest
from in3py.model.model import EnumsChains
from in3py.model.model import ModelUtils


def rpc_to_string(rpc:RPCRequest)->str:
    aux = rpc.__dict__
    aux["method"] = rpc.method.value
    aux["params"] = params_to_value(rpc.params)

    return json.dumps(aux)


def params_to_value(params):
    ret = []
    for p in params:
        ret.append(ModelUtils.to_json_rpc_param(p))
    return ret


def get_chain_by_id(id:str):
    for c in EnumsChains.__members__:
        if EnumsChains[c].value.chain_id == id:
            return EnumsChains[c]


