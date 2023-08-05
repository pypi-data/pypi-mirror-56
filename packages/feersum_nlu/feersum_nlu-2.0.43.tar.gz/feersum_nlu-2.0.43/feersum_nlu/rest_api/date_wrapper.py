"""
Wrapper of Feersum_NLU's Date Python API in HTTP API.
"""
from typing import Tuple, Optional  # noqa # pylint: disable=unused-import
# import uuid

from feersum_nlu.rest_api import wrapper_util


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def date_parse_text(iname: str, auth_token: str, caller_name: Optional[str],
                    text: Optional[str], lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    # name = iname + "_" + auth_token

    if text is None:
        return 400, {"error_detail": "No text to parse!"}  # Bad/Malformed request.

    # List[Tuple[str, str]]
    result_list = wrapper_util.get_nlpe_engine().retrieve_date(text, "future")

    return 200, result_list
