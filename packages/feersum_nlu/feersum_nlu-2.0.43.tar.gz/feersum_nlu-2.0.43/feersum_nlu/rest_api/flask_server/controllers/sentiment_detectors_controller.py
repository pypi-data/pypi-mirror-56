from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import sentiment_wrapper


@controller_util.controller_decorator
def sentiment_detector_retrieve(user, token_info,
                                instance_name, text_input):
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    text = text_input.get("text")
    lang_code = text_input.get("lang_code")

    response_code, response_json = \
        sentiment_wrapper.detect_sentiment(instance_name,
                                           auth_token=auth_token,
                                           caller_name=caller_name,
                                           text=text, lang_code=lang_code)
    return response_json, response_code
