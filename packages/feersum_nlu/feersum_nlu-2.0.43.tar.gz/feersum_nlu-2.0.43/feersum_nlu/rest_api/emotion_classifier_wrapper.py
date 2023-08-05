"""
Wrapper of Feersum_NLU's Emotion Classifier Python API in HTTP API.
"""
from typing import Tuple, Optional  # noqa # pylint: disable=unused-import

from feersum_nlu.rest_api import wrapper_util


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def emotion_clsfr_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                           text: Optional[str],
                           lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if text is None:
        return 400, {"error_detail": "No text provided!"}  # Bad/Malformed request.

    # name = iname + "_" + auth_token

    # [(label, score)], lang_code
    scored_label_list, lang_code = wrapper_util.get_nlpe_engine().retrieve_emotion(text, lang_code)

    return 200, scored_label_list
