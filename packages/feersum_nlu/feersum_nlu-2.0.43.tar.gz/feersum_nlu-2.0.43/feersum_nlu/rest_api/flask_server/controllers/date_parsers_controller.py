from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import date_wrapper


@controller_util.controller_decorator
def date_parser_retrieve(user, token_info, instance_name,
                         text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = \
        date_wrapper.date_parse_text("generic", auth_token=auth_token,
                                     caller_name=caller_name,
                                     text=text, lang_code=lang_code)

    if 200 <= response_code <= 299:
        result_dict_list = []
        result_list_list = response_json

        # Convert from tuple representation to dict representation!
        for value, grain in result_list_list:
            result_dict_list.append({'value': value, 'granularity': grain})

        return result_dict_list, response_code
    else:
        return response_json, response_code
