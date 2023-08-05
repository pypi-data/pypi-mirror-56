from typing import List, Tuple  # noqa # pylint: disable=unused-import

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import image_reader_wrapper


@controller_util.controller_decorator
def image_reader_retrieve(user, token_info,
                          instance_name, image_input):
    """
    Extract the text in the image.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param image_input: The base-64 encoded image OR image URL.
    :return: The list of extracted text [{"text": "...", "lang_code": "..."}].
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    image = image_input.get("image")
    url = image_input.get("url")

    response_code, response_json = image_reader_wrapper.image_reader_retrieve(instance_name,
                                                                              auth_token=auth_token,
                                                                              caller_name=caller_name,
                                                                              image=image,
                                                                              url=url)
    # [{"text": "...", "lang_code": "..."}]

    return response_json, response_code
