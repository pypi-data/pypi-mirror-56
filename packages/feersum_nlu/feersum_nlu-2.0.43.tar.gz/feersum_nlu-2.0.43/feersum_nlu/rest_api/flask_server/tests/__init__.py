import os
import sys
from typing import Optional

from flask_testing import TestCase

import json
from requests.models import Response

from feersum_nlu.rest_flask_utils import db, create_flask_app
from feersum_nlu.rest_flask_utils import create_celery_app

from feersum_nlu.rest_flask_utils import setup_logging, reset_logging

from feersum_nlu.rest_api.wrapper_util import load_shared_models as wrapper_load_shared_models

from feersum_nlu.rest_api.wrapper_util import start_nlp_engine as wrapper_start_nlp_engine
# from feersum_nlu.rest_api.wrapper_util import get_nlpe_engine as wrapper_get_nlp_engine
from feersum_nlu.rest_api.wrapper_util import start_vision_engine as wrapper_start_vision_engine  # noqa

if "PYCHARM_HOSTED" in os.environ:
    # NOTE: The below import is useful to bring feersum_nlu into the Python path when tests executed from within PyCharm!
    module_path = os.path.abspath(os.path.join('../../..'))
    print("module_path =", module_path)
    if module_path not in sys.path:
        sys.path.append(module_path)


class BaseTestCase(TestCase):
    def __init__(self, use_duckling: bool,
                 *args, **kwargs):
        self.use_duckling = use_duckling
        TestCase.__init__(self, *args, **kwargs)

    def create_app(self):
        setup_logging()

        # Local DB for testing - See 'local_db' make target.
        database_url = "postgresql://127.0.0.1:5432/test_feersumnlu?user=feersumnlu&password=feersumnlu"

        wrapper_start_nlp_engine(use_duckling=self.use_duckling)

        # Switch to env var / QA instance of duckling. Default is prod instance.
        # duckling_url = os.environ.get("FEERSUM_NLU_DUCKLING_URL", "https://qonda.qa.feersum.io")
        # wrapper_get_nlp_engine().set_duckling_url(duckling_url)

        wrapper_start_vision_engine()

        # Make a test app (includes debugging, etc.) with an API, but no UI.
        flask_app = create_flask_app(add_api=True, swagger_ui=False,
                                     database_url=database_url,
                                     debug=True)

        # celery_app = \
        create_celery_app(flask_app,
                          enable_background_training=False)

        wrapper_load_shared_models(lm_name_list=[],
                                   vm_name_list=[])

        return flask_app.app

    def setUp(self):
        print("Creating a test DB...", flush=True)
        db.create_all()

        print("done.", flush=True)

    def tearDown(self):
        print("Destroying the test DB...", flush=True)
        db.session.remove()
        db.drop_all()

        reset_logging()
        print("done.", flush=True)


def _check_set_response(response_list: list,
                        min_required_response_list: list,
                        treat_list_as_set: bool) -> bool:
    """
    Iterate over list values in the minimum required response and check against the actual response. Returns False
    on first mis-match.

    :param response_list: The response list to check recursively.
    :param min_required_response_list: The minimum required response.
    :return: False if mismatch found. True otherwise.
    """
    if len(response_list) < len(min_required_response_list):
        return False

    for min_required_value in min_required_response_list:
        min_required_value_count = 0

        for value in response_list:
            if _check_response(value, min_required_value, treat_list_as_set):
                min_required_value_count += 1  # Make sure to mutate the counter!
                break

        if min_required_value_count == 0:
            print("================================")
            print("=== CHECK_SET_RESPONSE ERROR ===")
            print("================================")
            print("Didn't find ", min_required_value)
            print("================================")
            return False

    return True


def _check_list_response(response_list: list,
                         min_required_response_list: list,
                         treat_list_as_set: bool) -> bool:
    """
    Iterate over list values in the minimum required response and check against the actual response. Returns False
    on first mis-match.

    :param response_list: The response list to check recursively.
    :param min_required_response_list: The minimum required response.
    :return: False if mismatch found. True otherwise.
    """
    if len(response_list) < len(min_required_response_list):
        return False

    min_required_list_len = len(min_required_response_list)

    for i in range(min_required_list_len):
        min_required_value = min_required_response_list[i]
        value = response_list[i]

        if not _check_response(value, min_required_value, treat_list_as_set):
            return False

    return True


def _check_dict_response(response_dict: dict,
                         min_required_response_dict: dict,
                         treat_list_as_set: bool) -> bool:
    """
    Iterate over json values in the minimum required response and check against the actual response. Returns False
    on first mis-match.

    :param response_dict: The response dict to check recursively.
    :param min_required_response_dict: The minimum required response.
    :return: False if mismatch found. True otherwise.
    """
    for key in min_required_response_dict:
        min_required_value = min_required_response_dict.get(key)
        value = response_dict.get(key)

        if min_required_value is not None and value is None:
            return False

        if not _check_response(value, min_required_value, treat_list_as_set):
            return False

    return True


def _check_response(response_value,
                    min_required_response_value,
                    treat_list_as_set: bool):
    """
    Recursive matching helper. Calls _check_dict_response and _check_list_response.

    :param response_value: The response check recursively.
    :param min_required_response_value: The minimum required response.
    :return: False if mismatch found. True otherwise.
    """
    if isinstance(min_required_response_value, list) and treat_list_as_set:
        if not isinstance(response_value, list):
            return False
        if not _check_set_response(response_value, min_required_response_value, treat_list_as_set):
            return False
    elif isinstance(min_required_response_value, list) and not treat_list_as_set:
        if not isinstance(response_value, list):
            return False
        if not _check_list_response(response_value, min_required_response_value, treat_list_as_set):
            return False
    elif isinstance(min_required_response_value, dict):
        if not isinstance(response_value, dict):
            return False
        if not _check_dict_response(response_value, min_required_response_value, treat_list_as_set):
            return False
    else:
        if isinstance(min_required_response_value, float):
            min_required_response_value = round(min_required_response_value, 1)
        if isinstance(response_value, float):
            response_value = round(response_value, 1)
        if min_required_response_value != response_value:
            return False

    return True


def check_response_request(client, endpoint: str, method: str,
                           request_data,
                           request_token: Optional[str] = None):
    """
    Send an api request and return the response.

    :param client: The requesting client.
    :param endpoint: The end-point to contact e.g. "/nlu/v2/dashboard".
    :param method: The request method.
    :param request_data: The data payload.
    :param request_token: An optional auth token to use instead of the default test token.
    :return: The status response.
    """
    try:
        request_data_string = json.dumps(request_data)
    except ValueError:
        request_data_string = ""

    if request_token is None:
        header = {"X-Auth-Token": "FEERSUM-NLU-591-4ba0-8905-996076e94d"}  # The token used for testing by default.
    else:
        header = {"X-Auth-Token": request_token}

    if method == "post":
        response = client.open(endpoint,
                               method="POST",
                               data=request_data_string,
                               content_type="application/json",
                               headers=header)
    elif method == "get":
        response = client.open(endpoint,
                               method="GET",
                               data=request_data_string,
                               content_type="application/json",
                               headers=header)
    elif method == "put":
        response = client.open(endpoint,
                               method="PUT",
                               data=request_data_string,
                               content_type="application/json",
                               headers=header)
    elif method == "delete":
        response = client.open(endpoint,
                               method="DELETE",
                               data=request_data_string,
                               content_type="application/json",
                               headers=header)
    else:
        response = Response()
        response.status_code = 405
        response.headers = {
            "Content-Type": "application/json"
        }

    return response


def check_response_test(response,
                        required_status_response: int,
                        min_required_response,
                        treat_list_as_set: bool = False) -> bool:
    """
    Test the response against the min_required_response.

    :param response: The api response.
    :param required_status_response: The required response status.
    :param min_required_response: The required json response. See below for why it is called min.
    :param treat_list_as_set: If False then the lists are tested for equivalence over the first k elements where k is the
                              minimum of the two lengths.
                              If True then the list are treated as sets and the equivalence requires that all the elements of
                              min_required_response exists in the request response.
                              Limitation - This applies to all lists in the response.
    :return: True if the response matches the min required response. False otherwise.
    """
    if response.status_code != required_status_response:
        print("============================")
        print("=== CHECK_RESPONSE ERROR ===")
        print("============================")
        print("response.status_code:")
        print(response.status_code)
        print("response:")
        print(str(response))
        print("required_status_response:")
        print(required_status_response)
        print("============================")
        print(flush=True)
        return False

    if len(min_required_response) > 0:
        try:
            response_data = json.loads(response.data.decode("utf-8"))
            if not _check_response(response_data, min_required_response, treat_list_as_set):
                print("============================")
                print("=== CHECK_RESPONSE ERROR ===")
                print("============================")
                print("response")
                print(str(response_data))
                print("min_required_response:")
                print(min_required_response)
                print("============================")
                print(flush=True)
                return False
        except ValueError:
            print("============================")
            print("++++++++ VALUE ERROR +++++++")
            print("=== CHECK_RESPONSE ERROR ===")
            print("============================")
            print("response:")
            print(str(response))
            print("min_required_response:")
            print(min_required_response)
            print("============================")
            print(flush=True)
            return False

    return True


def check_response(client, endpoint: str, method: str,
                   request_data,
                   required_status_response: int,
                   min_required_response,
                   treat_list_as_set: bool = False) -> bool:
    """
    Send a request and check the response against the min_required_response.

    :param client: The requesting client.
    :param endpoint: The end-point to contact e.g. "/nlu/v2/dashboard".
    :param method: The request method.
    :param request_data: The data payload.
    :param required_status_response: The required response status.
    :param min_required_response: The required json response. See below for why it is called min.
    :param treat_list_as_set: If False then the lists are tested for equivalence over the first k elements where k is the
                              minimum of the two lengths.
                              If True then the list are treated as sets and the equivalence requires that all the elements of
                              min_required_response exists in the request response.
                              Limitation - This applies to all lists in the response.
    :return: True if the response matches the min required response. False otherwise.
    """
    response = check_response_request(client, endpoint, method, request_data)

    return check_response_test(response, required_status_response, min_required_response, treat_list_as_set)
