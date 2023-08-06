"""
Pseudonymization function that utilizes a lookup table. The lookup table
comprise all possible outputs that an input val can be mapped to. The input
value is hashed and the modulus operator is used to determine which lookup
table entry the value will map to.
"""

from ssb_pseudonymization.exceptions import PseudoFuncError
from ssb_pseudonymization.util import validate_func_params
import hashlib
import sys

FUNC_NAME = "lookuptable"

CONFIG_PARAMS = {
    'table': {
        'desc': 'List of possible values',
        'mandatory': True
    }
}

MANDATORY_CONFIG_PARAMS = [p for p in CONFIG_PARAMS.keys() if CONFIG_PARAMS[p]['mandatory'] is True]


python_version = sys.version_info[0]
if python_version == 2:
    def onebyte_hash(s):
        return ord(hashlib.md5(s).digest()[0])
else:
    def onebyte_hash(s):
        return hashlib.md5(s.encode('utf-8')).digest()[0]


def apply(config, val):
    """ Pseudonymize using a lookup table.

    Example config:
    {
       'func': 'lookuptable',
       'table': ["foo", "bar", "baz"]
    }
    """
    validate_func_params(config, MANDATORY_CONFIG_PARAMS)
    table = config.get('table')
    if table is None or len(table) == 0:
        raise PseudoFuncError("pseudo 'table' parameter not initialized. Must be a non-empty array.")
    table_size = len(table)
    return table[onebyte_hash(val) % table_size]
