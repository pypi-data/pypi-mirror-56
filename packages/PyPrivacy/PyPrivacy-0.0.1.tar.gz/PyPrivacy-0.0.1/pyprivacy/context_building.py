from pyprivacy.user_secrets import UserSecrets
from pyprivacy.primitives.data_policy_pair import DataPolicyPair
from pyprivacy.primitives.policy_helpers.private_data import PrivateData
from pyprivacy.primitives.collection import Collection
import pprint
from pyprivacy.decorators import TransformDecorator
import types


def gen_module_namespace(base=None, libraries=None):
    import pkgutil
    import importlib

    importlib.invalidate_caches()

    module_namespace = dict()

    if base:
        prefix_name = base.__name__ + '.'
        for _, mod_name, is_pac in pkgutil.iter_modules(path=base.__path__):
            if not is_pac:
                module_namespace[mod_name] = importlib.import_module(prefix_name + mod_name)

    for library in libraries:
        module = importlib.import_module(library)
        for k, v in vars(module).items():
            if isinstance(v, types.FunctionType):
                decorator = TransformDecorator()
                vars(module)[k] = decorator(v)
        module_namespace[library] = module

    return module_namespace


# we only need to do this once per deployment.
module_namespace = gen_module_namespace()


def assemble_locals(result, users_secrets, app_id, debug=False):
    lcls = module_namespace

    def user(name: str) -> UserSecrets:
        return users_secrets[name]


    def new_collection():
        return Collection()

    def sample_dpp(data, policy):
        dpp = DataPolicyPair(policy=policy, name='test', token=None, username='test', private_data=None)
        dpp._data = data
        return dpp

    lcls['result'] = result
    lcls['private'] = PrivateData
    lcls['user'] = user
    lcls['new_collection'] = new_collection
    lcls['return_to_app'] = result.return_to_app

    if debug:
        # allow printing in the debug state
        lcls['pprint'] = pprint.pprint
        lcls['sample_dpp'] = sample_dpp

    return lcls
