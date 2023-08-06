from in3py.model.in3_model import IN3Config

class In3Client:
    """
    In3Client instance for IN3 functions and Ethereum

    """

    def __init__(self, in3_config:IN3Config=None):
        from in3py.ethereum.ethereum import Ethereum
        from in3py.in3.in3 import IN3

        self.in3 = IN3()
        self.eth = Ethereum()
        if in3_config is not None:
            self.in3.config(in3_config=in3_config)

