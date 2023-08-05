from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import health_wrapper

from typing import Tuple, Dict  # noqa # pylint: disable=unused-import
import logging


# @controller_util.controller_decorator  NOTE: Decorator not used for now; we want this call to be light and skip auth&count.
def health_get_status(user, token_info):
    """ Reports back 200 if possible i.e. if service is up. """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = health_wrapper.health_get_status(auth_token=auth_token,
                                                                    caller_name=caller_name)

    logging.info(f"health_controller.health_get_status: {response_code}")

    return response_json, response_code
