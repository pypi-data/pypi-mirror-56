"""
Pseudonymization function that utilizes format preserving encryption (FPE).
FPE refers to encryption in such a way that the resulting output (the ciphertext)
is in the same format as the input (the plaintext).
"""

from ssb_pseudonymization.exceptions import PseudoFuncError
from ssb_pseudonymization.util import validate_func_params
import pyffx
import string

FUNC_NAME = "fpe"

CONFIG_PARAMS = {
    'alphabet': {
        'desc': 'String with all possible characters that a val can be composed of',
        'mandatory': True
    },

    'key': {
        'desc': 'Secret key used by the FPE algorithm',
        'mandatory': True
    }
}

MANDATORY_CONFIG_PARAMS = [p for p in CONFIG_PARAMS.keys() if CONFIG_PARAMS[p]['mandatory'] is True]

def apply(config, val):
    """ Pseudonymize using format preserving encryption.

    Example config:
    {
        'func': 'fpe',
        'key': 'some-secret-key', 
        'alphabet': string.ascii_letters
    }
    """
    validate_func_params(config, MANDATORY_CONFIG_PARAMS)
    try:
        alphabet = config.get('alphabet', string.printable)
        e = pyffx.String(config['key'].encode("utf-8"), alphabet, length=len(val))
        return e.encrypt(val)
    except ValueError:
        raise PseudoFuncError("Could not pseudonymize '{0}'. Check alphabet compatibility ({1})".format(val, alphabet))
