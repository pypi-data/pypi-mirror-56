
class IN3BaseException(Exception):
    """ In3 Base Exception """
    pass


class IN3NumberFormatException(IN3BaseException):
    """ It's not a valid number, please informe a valid format as 0x123 (Hex), 123(Hex without x) or an integer """
    pass


class PrivateKeyNotFoundException(IN3BaseException):
    """ Private Key not found, you can add it in  a local variable """
    pass


class AddressFormatException(IN3BaseException):
    """ The address is not correct, please check it again. """
    pass

class HashFormatException(IN3BaseException):

    """ The hash is not correct, please check the hash and try it again """
    pass
