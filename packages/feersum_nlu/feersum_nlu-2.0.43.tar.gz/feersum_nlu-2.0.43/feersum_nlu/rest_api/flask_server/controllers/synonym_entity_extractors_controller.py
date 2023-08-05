from typing import Optional, Dict  # noqa # pylint: disable=unused-import

import connexion

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import entity_wrapper_synonym


@controller_util.controller_decorator
def synonym_entity_extractor_add_testing_samples(user, token_info,
                                                 instance_name, synonym_sample_list):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    for sample in synonym_sample_list:
        sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_add_testing_samples(iname=instance_name,
                                                                auth_token=auth_token,
                                                                caller_name=caller_name,
                                                                json_testing_samples=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_update_testing_samples(user, token_info,
                                                    instance_name, synonym_sample_list):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    for sample in synonym_sample_list:
        sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_update_testing_samples(iname=instance_name,
                                                                   auth_token=auth_token,
                                                                   caller_name=caller_name,
                                                                   json_testing_samples=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_add_training_samples(user, token_info,
                                                  instance_name, synonym_sample_list):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    for sample in synonym_sample_list:
        sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_add_training_samples(iname=instance_name,
                                                                 auth_token=auth_token,
                                                                 caller_name=caller_name,
                                                                 json_training_samples=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_update_training_samples(user, token_info,
                                                     instance_name, synonym_sample_list):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    for sample in synonym_sample_list:
        sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_update_training_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_training_samples=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_create(user, token_info,
                                    create_details):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    name = create_details.get("name")
    long_name = create_details.get("long_name")
    desc = create_details.get("desc")
    load_from_store = create_details.get("load_from_store")
    revision_uuid = create_details.get("revision_uuid")

    response_code, response_json = entity_wrapper_synonym.synonym_extr_create(iname=name,
                                                                              auth_token=auth_token,
                                                                              caller_name=caller_name,
                                                                              long_name=long_name,
                                                                              description=desc,
                                                                              load_from_store=load_from_store,
                                                                              revision_uuid=revision_uuid)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_del(user, token_info,
                                 instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = entity_wrapper_synonym.synonym_extr_del(instance_name,
                                                                           auth_token=auth_token,
                                                                           caller_name=caller_name,
                                                                           vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_vaporise(user, token_info,
                                      instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = entity_wrapper_synonym.synonym_extr_del(instance_name,
                                                                           auth_token=auth_token,
                                                                           caller_name=caller_name,
                                                                           vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_del_testing_samples(user, token_info,
                                                 instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    if connexion.request.is_json:
        synonym_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in synonym_sample_list:
            sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_remove_testing_samples(iname=instance_name,
                                                                   auth_token=auth_token,
                                                                   caller_name=caller_name,
                                                                   json_samples_to_delete=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_del_testing_samples_all(user, token_info,
                                                     instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_remove_testing_samples(iname=instance_name,
                                                                   auth_token=auth_token,
                                                                   caller_name=caller_name,
                                                                   json_samples_to_delete=None)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_del_training_samples(user, token_info,
                                                  instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []

    if connexion.request.is_json:
        synonym_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in synonym_sample_list:
            sample_list.append(sample)

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_remove_training_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_samples_to_delete=sample_list)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_del_training_samples_all(user, token_info,
                                                      instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_remove_training_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_samples_to_delete=None)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_details(user, token_info,
                                         instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = entity_wrapper_synonym.synonym_extr_get_details(instance_name,
                                                                                   auth_token=auth_token,
                                                                                   caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_details_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = entity_wrapper_synonym.synonym_extr_get_details_all(auth_token=auth_token,
                                                                                       caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_testing_samples(user, token_info,
                                                 instance_name,
                                                 index=None,
                                                 len=None):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_get_testing_samples(iname=instance_name,
                                                                auth_token=auth_token,
                                                                index=index,
                                                                length=len,
                                                                caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_training_samples(user, token_info,
                                                  instance_name,
                                                  index=None,
                                                  len=None):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_get_training_samples(iname=instance_name,
                                                                 auth_token=auth_token,
                                                                 index=index,
                                                                 length=len,
                                                                 caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_retrieve(user, token_info,
                                      instance_name, text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = entity_wrapper_synonym.synonym_extr_retrieve(instance_name,
                                                                                auth_token=auth_token,
                                                                                caller_name=caller_name,
                                                                                text=text, lang_code=lang_code)
    # response_json = [{"entity": "fault", "index": 31, "len": 6}, ...]
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_train(user, token_info,
                                   instance_name, train_details):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    if train_details is not None:
        weak_match_threshold = train_details.get("threshold")
        # immediate_mode = train_details.get("immediate_mode")
        # callback_url = train_details.get("callback_url")
    else:
        weak_match_threshold = None
        # immediate_mode = None
        # callback_url = None

    response_code, response_json = entity_wrapper_synonym.synonym_extr_train(instance_name,
                                                                             auth_token=auth_token,
                                                                             caller_name=caller_name,
                                                                             weak_match_threshold=weak_match_threshold)

    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_labels(user, token_info,
                                        instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_get_class_labels(instance_name,
                                                             auth_token=auth_token,
                                                             caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_set_params(user, token_info,
                                        instance_name, model_params):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    param_dict = {}

    for attribute, value in model_params.items():
        param_dict[attribute] = value

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_set_params(instance_name,
                                                       auth_token=auth_token,
                                                       caller_name=caller_name,
                                                       param_dict=param_dict)
    return response_json, response_code


@controller_util.controller_decorator
def synonym_entity_extractor_get_params(user, token_info,
                                        instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_synonym.synonym_extr_get_params(instance_name,
                                                       auth_token=auth_token,
                                                       caller_name=caller_name)
    return response_json, response_code
