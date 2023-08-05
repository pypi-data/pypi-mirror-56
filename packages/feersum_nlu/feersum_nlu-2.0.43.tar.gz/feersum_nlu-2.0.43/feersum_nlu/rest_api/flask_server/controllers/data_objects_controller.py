from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import data_object_wrapper


@controller_util.controller_decorator
def data_object_get_names_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_get_names_all(auth_token=auth_token,
                                                                                 caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def data_object_post(user, token_info,
                     instance_name,
                     data):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_post(iname=instance_name,
                                                                        auth_token=auth_token,
                                                                        caller_name=caller_name,
                                                                        object_data=data)
    return response_json, response_code


@controller_util.controller_decorator
def data_object_get_details(user, token_info,
                            instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_get_details(instance_name,
                                                                               auth_token=auth_token,
                                                                               caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def data_object_del(user, token_info,
                    instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_del(instance_name,
                                                                       auth_token=auth_token,
                                                                       caller_name=caller_name,
                                                                       vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def data_object_del_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_del_all(auth_token=auth_token,
                                                                           caller_name=caller_name,
                                                                           vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def data_object_vaporise(user, token_info,
                         instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_del(instance_name,
                                                                       auth_token=auth_token,
                                                                       caller_name=caller_name,
                                                                       vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def data_object_untrash(user, token_info,
                        instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = data_object_wrapper.data_object_undelete(instance_name,
                                                                            auth_token=auth_token,
                                                                            caller_name=caller_name)
    return response_json, response_code
