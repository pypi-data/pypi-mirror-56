from ssb_pseudonymization.func import fpe
from ssb_pseudonymization.func import lookuptable
from ssb_pseudonymization.exceptions import PseudoFuncInvalidConfigError
from ssb_pseudonymization.exceptions import PseudoFuncError
import sys
import json

# All available pseudo functions
FUNCS = {
    fpe.FUNC_NAME: fpe.apply,
    lookuptable.FUNC_NAME: lookuptable.apply
}


def invoke(config_json, params):
    """ Invoke pseudonymization function specified in config file. """
    config = json.loads(config_json)
    func_name = config.get('func')
    if func_name is None:
        raise PseudoFuncInvalidConfigError("pseudo 'func' parameter not specified")

    pseudo_func = FUNCS.get(func_name)
    if pseudo_func is None:
        raise PseudoFuncError("unknown pseudo function: {0}".format(func_name))

    return pseudo_func(config, params)
