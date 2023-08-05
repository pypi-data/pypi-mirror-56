from typing import Optional, Dict  # noqa # pylint: disable=unused-import

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import api_key_wrapper


@controller_util.controller_decorator
def api_key_create(user, token_info,
                   create_details):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    desc = create_details.get("desc")
    call_count_limit = create_details.get("call_count_limit")

    response_code, response_json = api_key_wrapper.api_key_create(auth_token=auth_token,
                                                                  caller_name=caller_name,
                                                                  description=desc,
                                                                  call_count_limit=call_count_limit)
    # api_key, desc, call_count, call_count_limit
    return response_json, response_code


@controller_util.controller_decorator
def api_key_update_details(user, token_info,
                           instance_name,
                           create_details):
    """
    Update or add a key with api_key = instance name.
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    desc = create_details.get("desc")
    call_count_limit = create_details.get("call_count_limit")

    response_code, response_json = api_key_wrapper.api_key_update_details(instance_name,  # The API key.
                                                                          auth_token=auth_token,
                                                                          caller_name=caller_name,
                                                                          description=desc,
                                                                          call_count_limit=call_count_limit)
    # api_key, desc, call_count, call_count_limit
    return response_json, response_code


@controller_util.controller_decorator
def api_key_del(user, token_info,
                instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = api_key_wrapper.api_key_del(instance_name,  # The API key.
                                                               auth_token=auth_token,
                                                               caller_name=caller_name,
                                                               vaporise=False)
    # api_key, desc, call_count, call_count_limit
    return response_json, response_code


@controller_util.controller_decorator
def api_key_vaporise(user, token_info,
                     instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = api_key_wrapper.api_key_del(instance_name,  # The API key.
                                                               auth_token=auth_token,
                                                               caller_name=caller_name,
                                                               vaporise=True)
    # api_key, desc, call_count, call_count_limit
    return response_json, response_code


# ======
# ======
# ======

@controller_util.controller_decorator
def api_key_get_details(user, token_info,
                        instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = api_key_wrapper.api_key_get_details(instance_name,  # The API key.
                                                                       auth_token=auth_token,
                                                                       caller_name=caller_name)
    # api_key, desc, call_count, call_count_limit
    return response_json, response_code


@controller_util.controller_decorator
def api_key_get_details_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = api_key_wrapper.api_key_get_details_all(auth_token=auth_token,
                                                                           caller_name=caller_name)
    # [api_key, desc, call_count, call_count_limit]
    return response_json, response_code
