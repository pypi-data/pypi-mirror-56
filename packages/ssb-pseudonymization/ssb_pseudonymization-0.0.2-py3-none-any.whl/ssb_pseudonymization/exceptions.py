
class PseudoFuncInvalidConfigError(Exception):
    """ Raised if a pseudo function encounters invalid config, such as missing a mandatory param """
    pass

class PseudoFuncError(Exception):
    """ Raised if an error is encountered during pseudonymization """
    pass
