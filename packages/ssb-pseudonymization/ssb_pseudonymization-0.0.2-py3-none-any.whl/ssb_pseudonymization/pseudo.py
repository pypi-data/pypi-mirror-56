import pyffx
import string
import sys
import json
import hashlib


PSEUDO_FUNCTIONS = {
    'pseudop_fpe': pseudop_fpe,
    'pseudop_lookuptable': pseudop_lookuptable
}

class PseudoOpError(Exception):
    """ Exception thrown by pseudo operators """
    pass

try:
    # Python 2; Python 3 will throw an exception here as bytes are required
    def onebyte_hash(s):
        return ord(hashlib.md5(s).digest()[0])
except TypeError:
    # Python 3; encode the string first, return first byte
    def onebyte_hash(s):
        return hashlib.md5(s.encode('utf8')).digest()[0]


def pseudop_fpe(config, val):
    """ Pseudonymize using format preserving encryption.

    Example config:
    {
        'op': 'pseudop_fpe',
        'key': 'some-secret-key', 
        'alphabet': string.ascii_letters
    }
    """
    try:
        alphabet = config.get('alphabet', string.printable)
        e = pyffx.String(bytes(config['key']), alphabet, length=len(val))
        return e.encrypt(val)
    except ValueError:
        raise PseudoOpError("Could not pseudonymize '{0}'. Check alphabet compatibility ({1})".format(val, alphabet))


def pseudop_lookuptable(config, val):
    """ Pseudonymize using a lookup table.

    Example config:
    {
       'op': 'pseudop_lookuptable',
       'table': ["foo", "bar", "baz"]
    }
    """
    table = config.get('table')
    if table is None or len(table) == 0:
        raise PseudoOpError("pseudo 'table' parameter not initialized. Must be a non-empty array.")
    table_size = len(table)
    return table[onebyte_hash(val) % table_size]


def invoke_pseudo(config_json, params):
    """ Invoke pseudonymization operator specified in config file. """
    config = json.loads(config_json)
    op_name = config.get('op')
    if op_name is None:
        raise PseudoOpError("pseudo 'op' parameter not specified")
    
    op = PSEUDO_FUNCTIONS.get(op_name)
    if op is None:
        raise PseudoOpError("unknown pseudo operation: {0}".format(op_name))

    return op(config, params)
