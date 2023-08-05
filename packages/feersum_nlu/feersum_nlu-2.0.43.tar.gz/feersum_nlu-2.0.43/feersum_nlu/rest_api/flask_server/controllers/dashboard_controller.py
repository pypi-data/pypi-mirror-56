from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import dashboard_wrapper


@controller_util.controller_decorator
def dashboard_get_details(user, token_info):

    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = dashboard_wrapper.dashboard_get_details(auth_token=auth_token,
                                                                           caller_name=caller_name,
                                                                           show_data_objects=None,
                                                                           history_size=None)
    return response_json, response_code


@controller_util.controller_decorator
def dashboard_get_details_with_params(user, token_info,
                                      params):

    show_data_objects = params.get("show_data_objects")
    history_size = params.get("history_size")

    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = dashboard_wrapper.dashboard_get_details(auth_token=auth_token,
                                                                           caller_name=caller_name,
                                                                           show_data_objects=show_data_objects,
                                                                           history_size=history_size)
    return response_json, response_code
