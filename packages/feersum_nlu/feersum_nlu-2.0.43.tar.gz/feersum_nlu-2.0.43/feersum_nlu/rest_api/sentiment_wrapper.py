"""
Wrapper of Feersum_NLU's Sentiment Python API in HTTP API.
"""
from typing import Tuple, Optional  # noqa # pylint: disable=unused-import
# import uuid

from feersum_nlu.rest_api import wrapper_util


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def detect_sentiment(iname: str, auth_token: str, caller_name: Optional[str],
                     text: Optional[str],
                     lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if text is None:
        return 400, {"error_detail": "No text provided!"}  # Bad/Malformed request.

    # name = iname + "_" + auth_token

    sentiment, sentiment_detail = wrapper_util.get_nlpe_engine().retrieve_sentiment(text, lang_code)

    if sentiment_detail is None:
        return 200, {"value": sentiment}
    else:
        return 200, {"value": sentiment, "detail_list": sentiment_detail}
