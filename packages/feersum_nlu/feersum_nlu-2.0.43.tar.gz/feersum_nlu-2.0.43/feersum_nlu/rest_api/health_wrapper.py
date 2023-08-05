"""
Wrapper of Feersum_NLU's Dashboard Python API in HTTP API.
"""

from typing import Tuple, Optional  # noqa # pylint: disable=unused-import
import logging
# import json

from feersum_nlu.rest_api import wrapper_util


@wrapper_util.lock_decorator_health
@wrapper_util.auth_decorator
def health_get_status(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    logging.info(f"health_wrapper.health_get_status: Checking ...")

    model_info_list = wrapper_util.load_model_list(
        auth_token=auth_token,
        show_data_objects=False)  # List[Tuple[name, uuid, trashed, desc, long_name]]

    logging.info(f"health_wrapper.health_get_status: OK! ({len(model_info_list)} models)")

    return 200, {}  # Return 200 if no exceptions thrown on this typical API call path.
