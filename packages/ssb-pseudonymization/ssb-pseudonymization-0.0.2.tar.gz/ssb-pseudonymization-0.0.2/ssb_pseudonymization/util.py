from ssb_pseudonymization.exceptions import PseudoFuncInvalidConfigError


def validate_func_params(config_dict, mandatory_params_list):
    config_dict = {k: v for k, v in config_dict.items() if v is not None}
    missing = set(mandatory_params_list).difference(set(config_dict.keys()))
    if (len(missing) > 0):
        raise PseudoFuncInvalidConfigError('Missing mandatory config params: {}'.format( missing))
