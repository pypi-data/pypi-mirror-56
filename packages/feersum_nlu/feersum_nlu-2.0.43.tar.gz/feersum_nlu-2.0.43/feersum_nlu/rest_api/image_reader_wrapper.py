"""
Wrapper of Feersum_NLU's Image Reader Python API in HTTP API.
"""
from typing import Tuple, Optional  # noqa # pylint: disable=unused-import

import logging
import requests
# import time

from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import image_utils


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_reader_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                          image: Optional[str],
                          url: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if (image is None) and (url is None):
        return 400, {"error_detail": "No image provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    # success = image_clsfr_load_helper(name, look_in_trash=False)
    # meta_info = wrapper_util.image_classifier_dict.get(name)

    # if not success or meta_info is None:
    #     return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if image is not None:
        format_ok = image_utils.check_image_format(image, ignore_resolution=True)

        if format_ok is False:
            return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s
    elif url is not None:
        try:
            # Get image from url e.g. "https://www.googleapis.com/storage/v1/b/bucket_name/o/blob_name?alt=media"
            response = requests.get(url, timeout=8.0)
            image = image_utils.load_image_from_bytes(response.content, ignore_resolution=True)
            format_ok = image_utils.check_image_format(image, ignore_resolution=True)  # load SHOULD have reformat the image.

            if format_ok is False:
                return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.

            # Log the url for later debugging and maybe training.
            logging.info(f"image_reader_wrapper.image_reader_retrieve: url={url}.")
        except IOError:  # includes requests.exceptions.Timeout:
            return 400, {"error_detail": f"Couldn't get an image from {url} - IOError or Timeout!"}  # Bad/Malformed request.
    else:
        return 400, {"error_detail": "No image provided!"}  # Bad/Malformed request.

    image_utils.save_image("image_reader_wrapper_input.jpg", image)

    # returns [{"text": "...", "lang_code": "..."}]
    text_list = wrapper_util.get_vision_engine().retrieve_image_text(name, image)

    return 200, text_list
