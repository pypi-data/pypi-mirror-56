from pyprivacy.primitives.result import Result
from RestrictedPython import safe_builtins, compile_restricted_exec
from RestrictedPython.Eval import default_guarded_getitem
import traceback
import redis
from collections import namedtuple
import logging
from pyprivacy.context_building import assemble_locals

logger = logging.getLogger(__name__)

UserInfoBundle = namedtuple("UserInfoBundle", ['username', 'policies',
                                               'tokens', 'private_data'])


def execute(users_secrets, program, app_id=None, app_module=None):
    json_output = dict()
    # object to interact with the program
    result = Result()

    glbls = {'__builtins__': safe_builtins,
             '_getitem_': default_guarded_getitem
             }

    lcls = assemble_locals(result=result,
                           users_secrets=users_secrets,
                           app_id=app_id,
                           debug=True)
    try:
        c_program = compile_restricted_exec(program)
        exec(c_program, glbls, lcls)

    except:
        print(traceback.format_exc())
        json_output = {'result': 'error', 'traceback': traceback.format_exc()}
        return json_output

    json_output['stored_items'] = result._stored_keys
    json_output['encrypted_data'] = result._encrypted_data
    json_output['data'] = result._dp_pair_data
    json_output['result'] = 'ok'
    return json_output
