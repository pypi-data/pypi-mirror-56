from in3py.model.model import IN3Config

""" Testing documentation  here """
class In3Client:
    """
    Testing  here my init function

    Returns
    -------
    in3
        IN3 instance

    """
    def __init__(self, in3_config:IN3Config=None):
        from in3py.ethereum.ethereum import Ethereum
        from in3py.in3.in3 import IN3

        self.in3 = IN3()
        self.eth = Ethereum()
        if in3_config is not None:
            self.in3.config(in3_config=in3_config)

