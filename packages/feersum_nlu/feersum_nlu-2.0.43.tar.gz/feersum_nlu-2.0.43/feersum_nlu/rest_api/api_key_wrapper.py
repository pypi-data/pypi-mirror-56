"""
Wrapper of Feersum_NLU's API key Python API in HTTP API.
"""
from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
import uuid

from feersum_nlu.rest_api import wrapper_util


# ======================== #
# === Start of helpers === #
# ======================== #

# ======================== #
# ======================== #
# ======================== #


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def api_key_create(auth_token: str, caller_name: Optional[str],
                   description: str,
                   call_count_limit: Optional[int]) -> Tuple[int, wrapper_util.JSONType]:
    if description is None or description == "":
        return 400, {"error_detail": "No description provided!"}  # Bad/Malformed request.

    # Check for admin token
    if not wrapper_util.is_admin_auth_token_valid(auth_token):
        # Bad/Malformed request.
        return 400, {"error_detail": "Invalid authorisation token provided! Managing API keys require special permission!"}

    # Create an API key
    api_key = str(uuid.uuid4())

    details = {
        "api_key": api_key,
        "desc": description,
        "call_count": 0,
        "call_count_limit": call_count_limit,
        "call_count_breakdown": {}
    }
    # Add new key to keys table; if call_count_limit is None then there is no call_count_limit.
    wrapper_util.add_auth_token(api_key,
                                description,
                                call_count_limit)

    # Return api_key, desc, call_count, call_count_limit
    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def api_key_update_details(iname: str, auth_token: str, caller_name: Optional[str],
                           description: str,
                           call_count_limit: Optional[int]) -> Tuple[int, wrapper_util.JSONType]:
    """
    Update or add a key with api_key = iname.
    """
    if iname is None:
        return 400, {"error_detail": "No API key provided!"}  # Bad/Malformed request.

    # Check for admin token
    if not wrapper_util.is_admin_auth_token_valid(auth_token):
        # Bad/Malformed request.
        return 400, {"error_detail": "Invalid authorisation token provided! Managing API keys require special permission!"}

    api_key = iname
    api_key_details = wrapper_util.get_auth_token_details(api_key)

    if api_key_details is None:
        # API key doesn't exist yet so add a new key.
        if description is None or description == "":
            return 400, {"error_detail": "This is a new key, a description should be provided!"}  # Bad/Malformed request.

        details = {
            "api_key": api_key,
            "desc": description,
            "call_count": 0,
            "call_count_limit": call_count_limit,
            "call_count_breakdown": {}
        }
        # Add the new key.
        wrapper_util.add_auth_token(api_key,
                                    description,
                                    call_count_limit)
    else:
        # API key already exists so update its details.
        details = {
            "api_key": api_key,
            "desc": api_key_details.get("desc") if description is None else description,
            "call_count": api_key_details.get("call_count", 0),
            "call_count_limit": call_count_limit,
            "call_count_breakdown": api_key_details.get("call_count_breakdown")
        }
        # Add the key with updated details; replaces old entry.
        wrapper_util.add_auth_token(api_key, details.get('desc'),  # type: ignore
                                    call_count_limit)

    # Return api_key, desc, call_count, call_count_limit
    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def api_key_del(iname: str, auth_token: str, caller_name: Optional[str],
                vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the api key. """
    if iname is None:
        return 400, {"error_detail": "No API key provided!"}  # Bad/Malformed request.

    # Check for admin token
    if not wrapper_util.is_admin_auth_token_valid(auth_token):
        # Bad/Malformed request.
        return 400, {"error_detail": "Invalid authorisation token provided! Managing API keys require special permission!"}

    api_key_details = wrapper_util.get_auth_token_details(iname)

    if api_key_details is None:
        # Bad/Malformed request.
        return 400, {"error_detail": f"API key {iname} not found!"}

    success = wrapper_util.remove_auth_token(iname)

    if success is False:
        # Bad/Malformed request.
        return 400, {"error_detail": f"Could not delete API key {iname}!"}

    details = {
        "api_key": iname,
        "desc": api_key_details.get("desc"),
        "call_count": api_key_details.get("call_count"),
        "call_count_limit": api_key_details.get("call_count_limit"),
        "call_count_breakdown": api_key_details.get("call_count_breakdown")
    }

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def api_key_get_details(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No API key provided!"}  # Bad/Malformed request.

    # Check for admin token
    # NOTE: CHECK NOT NEEDED - Since keys are secret you can actually be allowed to get info on any key you know!
    # if not wrapper_util.is_admin_auth_token_valid(auth_token):
    #     # Bad/Malformed request.
    #     return 400, {"error_detail": "Invalid authorisation token provided! Managing API keys require special permission!"}

    api_key_details = wrapper_util.get_auth_token_details(iname)

    if api_key_details is None:
        # Bad/Malformed request.
        return 400, {"error_detail": f"API key {iname} not found!"}

    details = {
        "api_key": iname,
        "desc": api_key_details.get("desc"),
        "call_count": api_key_details.get("call_count"),
        "call_count_limit": api_key_details.get("call_count_limit"),
        "call_count_breakdown": api_key_details.get("call_count_breakdown")
    }

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def api_key_get_details_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    # Check for admin token
    if not wrapper_util.is_admin_auth_token_valid(auth_token):
        # Bad/Malformed request.
        return 400, {"error_detail": "Invalid authorisation token provided! Managing API keys require special permission!"}

    details_list = []  # type: List[Dict]

    api_keys = wrapper_util.load_auth_token_list()

    for iname in api_keys:
        api_key_details = wrapper_util.get_auth_token_details(iname)

        if api_key_details is not None:
            details = {
                "api_key": iname,
                "desc": api_key_details.get("desc"),
                "call_count": api_key_details.get("call_count"),
                "call_count_limit": api_key_details.get("call_count_limit"),
                "call_count_breakdown": api_key_details.get("call_count_breakdown")
            }

            details_list.append(details)

    # Return api_key, desc, call_count, call_count_limit
    return 200, details_list
