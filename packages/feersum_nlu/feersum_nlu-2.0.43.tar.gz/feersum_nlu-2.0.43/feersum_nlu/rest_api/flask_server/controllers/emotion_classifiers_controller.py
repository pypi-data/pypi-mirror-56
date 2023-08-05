from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import emotion_classifier_wrapper


@controller_util.controller_decorator
def emotion_classifier_retrieve(user, token_info,
                                instance_name, text_input):
    """
    Make a prediction.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param text_input:
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = emotion_classifier_wrapper.emotion_clsfr_retrieve(instance_name,
                                                                                     auth_token=auth_token,
                                                                                     caller_name=caller_name,
                                                                                     text=text, lang_code=lang_code)
    # response_json = List[Tuple[label, score]

    if 200 <= response_code <= 299:
        result_tuple_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in result_tuple_list:
            # result is [label, score]
            result_dict_list.append({"label": result[0], "probability": result[1]})

        return result_dict_list, response_code
    else:
        return response_json, response_code
