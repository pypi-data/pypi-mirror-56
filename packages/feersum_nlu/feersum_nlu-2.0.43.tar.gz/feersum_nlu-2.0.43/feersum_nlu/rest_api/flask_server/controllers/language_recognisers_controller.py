from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import language_recogniser_wrapper


@controller_util.controller_decorator
def language_recogniser_create(user, token_info,
                               create_details):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    name = create_details.get("name")
    long_name = create_details.get("long_name")
    desc = create_details.get("desc")
    lid_model_file = create_details.get("lid_model_file")
    load_from_store = create_details.get("load_from_store")
    revision_uuid = create_details.get("revision_uuid")

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_create(iname=name,
                                                                   auth_token=auth_token,
                                                                   caller_name=caller_name,
                                                                   long_name=long_name,
                                                                   description=desc,
                                                                   lid_model_file=lid_model_file,
                                                                   load_from_store=load_from_store,
                                                                   revision_uuid=revision_uuid)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_del(user, token_info,
                            instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_del(instance_name,
                                                                auth_token=auth_token,
                                                                caller_name=caller_name,
                                                                vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_vaporise(user, token_info,
                                 instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_del(instance_name,
                                                                auth_token=auth_token,
                                                                caller_name=caller_name,
                                                                vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_get_details(user, token_info,
                                    instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_get_details(instance_name,
                                                                        auth_token=auth_token,
                                                                        caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_get_details_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_get_details_all(auth_token=auth_token,
                                                                            caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_retrieve(user, token_info,
                                 instance_name, text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_retrieve(instance_name,
                                                                     auth_token=auth_token,
                                                                     caller_name=caller_name,
                                                                     text=text, lang_code=lang_code)

    if 200 <= response_code <= 299:
        result_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in result_list_list:
            result_dict_list.append({"label": result[0], "probability": result[1]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def lr4_language_recogniser_retrieve(user, token_info,
                                     instance_name, text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_retrieve(instance_name,
                                                                     auth_token=auth_token,
                                                                     caller_name=caller_name,
                                                                     text=text, lang_code=lang_code)

    if 200 <= response_code <= 299:
        result_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in result_list_list:
            result_dict_list.append({"label": result[0], "probability": result[1]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_set_params(user, token_info,
                                   instance_name, model_params):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    param_dict = {}

    for attribute, value in model_params.items():
        param_dict[attribute] = value

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_set_params(instance_name,
                                                                       auth_token=auth_token,
                                                                       caller_name=caller_name,
                                                                       param_dict=param_dict)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_get_params(user, token_info,
                                   instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_get_params(instance_name,
                                                                       auth_token=auth_token,
                                                                       caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def language_recogniser_get_labels(user, token_info,
                                   instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        language_recogniser_wrapper.lr4_language_recogniser_get_class_labels(instance_name,
                                                                             auth_token=auth_token,
                                                                             caller_name=caller_name)
    return response_json, response_code
