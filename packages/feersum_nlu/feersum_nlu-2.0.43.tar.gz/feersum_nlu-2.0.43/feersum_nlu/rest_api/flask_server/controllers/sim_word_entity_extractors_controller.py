from typing import Optional, Set, Any  # noqa # pylint: disable=unused-import

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import entity_wrapper_similar_word


@controller_util.controller_decorator
def sim_word_entity_extractor_create(user, token_info,
                                     create_details):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    name = create_details.get("name")
    long_name = create_details.get("long_name")
    desc = create_details.get("desc")
    similar_word_list = create_details.get("similar_words")
    threshold = create_details.get("threshold", )
    word_manifold = create_details.get("word_manifold")
    load_from_store = create_details.get("load_from_store")
    revision_uuid = create_details.get("revision_uuid")

    similar_word_set = None  # type: Optional[Set[Any]]

    if similar_word_list is not None:
        similar_word_set = set(similar_word_list)

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_create(iname=name,
                                                         auth_token=auth_token,
                                                         caller_name=caller_name,
                                                         long_name=long_name,
                                                         description=desc,
                                                         input_entities=similar_word_set,
                                                         threshold=threshold,
                                                         word_manifold_name=word_manifold,
                                                         load_from_store=load_from_store,
                                                         revision_uuid=revision_uuid)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_del(user, token_info,
                                  instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_del(instance_name,
                                                      auth_token=auth_token,
                                                      caller_name=caller_name,
                                                      vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_vaporise(user, token_info,
                                       instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_del(instance_name,
                                                      auth_token=auth_token,
                                                      caller_name=caller_name,
                                                      vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_get_details(user, token_info,
                                          instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_get_details(instance_name,
                                                              auth_token=auth_token,
                                                              caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_get_details_all(user, token_info):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_get_details_all(auth_token=auth_token,
                                                                  caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_retrieve(user, token_info,
                                       instance_name, text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_retrieve(instance_name,
                                                           auth_token=auth_token,
                                                           caller_name=caller_name,
                                                           text=text, lang_code=lang_code)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_set_params(user, token_info,
                                         instance_name, model_params):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    param_dict = {}

    for attribute, value in model_params.items():
        param_dict[attribute] = value

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_set_params(instance_name,
                                                             auth_token=auth_token,
                                                             caller_name=caller_name,
                                                             param_dict=param_dict)
    return response_json, response_code


@controller_util.controller_decorator
def sim_word_entity_extractor_get_params(user, token_info,
                                         instance_name):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        entity_wrapper_similar_word.sim_word_extr_get_params(instance_name,
                                                             auth_token=auth_token,
                                                             caller_name=caller_name)
    return response_json, response_code
