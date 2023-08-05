from typing import Optional, Dict, List, Tuple  # noqa # pylint: disable=unused-import

import connexion

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import faq_wrapper


@controller_util.controller_decorator
def faq_matcher_add_testing_samples(user, token_info,
                                    instance_name, labelled_text_sample_list):
    """
    Add testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_text_sample_list: ["text":, "label":, "lang_code":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str]]

    for sample in labelled_text_sample_list:
        lang_code = sample.get("lang_code", "")  # If lang_code isn't given then lang_ident must be run during testing
        sample_list.append((sample.get("text"), sample.get("label"), lang_code))

    response_code, response_json = \
        faq_wrapper.faq_add_testing_samples(iname=instance_name,
                                            auth_token=auth_token,
                                            caller_name=caller_name,
                                            json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_update_testing_samples(user, token_info,
                                       instance_name, labelled_text_sample_list):
    """
    Update testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_text_sample_list: ["text":, "label":, "lang_code":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str, str]]

    for sample in labelled_text_sample_list:
        lang_code = sample.get("lang_code", "")  # If lang_code isn't given then lang_ident must be run during testing
        sample_list.append((sample.get("text"), sample.get("label"), lang_code, sample.get("uuid")))

    response_code, response_json = \
        faq_wrapper.faq_update_testing_samples(iname=instance_name,
                                               auth_token=auth_token,
                                               caller_name=caller_name,
                                               json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_add_training_samples(user, token_info,
                                     instance_name, labelled_text_sample_list):
    """
    Add testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_text_sample_list: ["text":, "label":, "lang_code":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str]]

    for sample in labelled_text_sample_list:
        lang_code = sample.get("lang_code", "")  # If lang_code isn't given then lang_ident must be run during training
        sample_list.append((sample.get("text"), sample.get("label"), lang_code))

    response_code, response_json = \
        faq_wrapper.faq_add_training_samples(iname=instance_name,
                                             auth_token=auth_token,
                                             caller_name=caller_name,
                                             json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_update_training_samples(user, token_info,
                                        instance_name, labelled_text_sample_list):
    """
    Update testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_text_sample_list: ["text":, "label":, "lang_code":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str, str]]

    for sample in labelled_text_sample_list:
        lang_code = sample.get("lang_code", "")  # If lang_code isn't given then lang_ident must be run during training
        sample_list.append((sample.get("text"), sample.get("label"), lang_code, sample.get("uuid")))

    response_code, response_json = \
        faq_wrapper.faq_update_training_samples(iname=instance_name,
                                                auth_token=auth_token,
                                                caller_name=caller_name,
                                                json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_create(user, token_info,
                       create_details):
    """
    Creat a new model or load_from_store i.e. load from the trash!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param create_details: Details like name, long_name and desc. The classifier and languages are chosen at training time!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    name = create_details.get("name")
    long_name = create_details.get("long_name")
    desc = create_details.get("desc")
    load_from_store = create_details.get("load_from_store")
    revision_uuid = create_details.get("revision_uuid")

    response_code, response_json = faq_wrapper.faq_create(iname=name,
                                                          auth_token=auth_token,
                                                          caller_name=caller_name,
                                                          long_name=long_name,
                                                          description=desc,
                                                          load_from_store=load_from_store,
                                                          revision_uuid=revision_uuid)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_del(user, token_info,
                    instance_name):
    """
    Move the model to the trash. To un-trash use 'create' with load from store = True.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_del(instance_name,
                                                       auth_token=auth_token,
                                                       caller_name=caller_name,
                                                       vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_vaporise(user, token_info,
                         instance_name):
    """
    Permanently delete a model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_del(instance_name,
                                                       auth_token=auth_token,
                                                       caller_name=caller_name,
                                                       vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_del_testing_samples(user, token_info,
                                    instance_name):
    """
    Flask controller endpoint to delete testing samples from a text classifier.

    Flask controller endpoint to delete testing samples from a text classifier. NOTE: The payload of an
    http DEL request is used here!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]

    # Note: The payload of an http DEL request is used here!
    if connexion.request.is_json:
        labelled_text_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in labelled_text_sample_list:
            lang_code = sample.get("lang_code", "")
            sample_list.append((sample.get("text"), sample.get("label"),
                                lang_code,
                                sample.get("uuid")))

    response_code, response_json = \
        faq_wrapper.faq_remove_testing_samples(iname=instance_name,
                                               auth_token=auth_token,
                                               caller_name=caller_name,
                                               json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_del_testing_samples_all(user, token_info,
                                        instance_name):
    """
    Del all the testing samples.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_remove_testing_samples(iname=instance_name,
                                               auth_token=auth_token,
                                               caller_name=caller_name,
                                               json_testing_data=None)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_del_training_samples(user, token_info,
                                     instance_name):
    """
    Flask controller endpoint to delete testing samples from a text classifier.

    Flask controller endpoint to delete testing samples from a text classifier. NOTE: The payload of an
    http DEL request is used here!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]

    # Note: The payload of an http DEL request is used here!
    if connexion.request.is_json:
        labelled_text_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in labelled_text_sample_list:
            lang_code = sample.get("lang_code", "")
            sample_list.append((sample.get("text"), sample.get("label"),
                                lang_code,
                                sample.get("uuid")))

    response_code, response_json = \
        faq_wrapper.faq_remove_training_samples(iname=instance_name,
                                                auth_token=auth_token,
                                                caller_name=caller_name,
                                                json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_del_training_samples_all(user, token_info,
                                         instance_name):
    """
    Del all the training samples.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_remove_training_samples(iname=instance_name,
                                                auth_token=auth_token,
                                                caller_name=caller_name,
                                                json_training_data=None)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


# ======
# ======
# ======

@controller_util.controller_decorator
def faq_matcher_get_details(user, token_info,
                            instance_name):
    """
    Get the details of the named instance.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_get_details(instance_name,
                                                               auth_token=auth_token,
                                                               caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_get_details_all(user, token_info):
    """
    Get details for all your text classifiers.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_get_details_all(auth_token=auth_token,
                                                                   caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_get_testing_samples(user, token_info,
                                    instance_name,
                                    index=None,
                                    len=None):
    """
    Get the model's testing data.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_get_testing_samples(iname=instance_name,
                                            auth_token=auth_token,
                                            index=index,
                                            length=len,
                                            caller_name=caller_name)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_get_training_samples(user, token_info,
                                     instance_name,
                                     index=None,
                                     len=None):
    """
    Get the model's training data.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param index: The sample index to start from.
    :param len: The number of samples to return.
    :return: The list of labelled samples.
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_get_training_samples(iname=instance_name,
                                             auth_token=auth_token,
                                             index=index,
                                             length=len,
                                             caller_name=caller_name)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_retrieve(user, token_info,
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

    response_code, response_json = faq_wrapper.faq_retrieve(instance_name,
                                                            auth_token=auth_token,
                                                            caller_name=caller_name,
                                                            text=text, lang_code=lang_code)
    # response_json = List[Tuple[text, answer_id, answer text/label, score, text_lang]]

    if 200 <= response_code <= 299:
        result_tuple_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in result_tuple_list:
            # result is [text, answer_id, answer text/label, score, text_lang]
            result_dict_list.append({"label": result[2], "probability": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_train(user, token_info,
                      instance_name, train_details):
    """
    Train the classifier using the specified algorithm and languages.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param train_details:
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    if train_details is not None:
        weak_match_threshold = train_details.get("threshold")

        word_manifold = train_details.get("word_manifold")
        word_manifold_list = train_details.get("word_manifold_list")

        immediate_mode = train_details.get("immediate_mode")
        callback_url = train_details.get("callback_url")
    else:
        weak_match_threshold = None
        word_manifold = None
        word_manifold_list = None
        immediate_mode = None
        callback_url = None

    word_manifold_dict = None  # type: Optional[Dict[str, str]]

    if word_manifold is not None:
        word_manifold_dict = {"eng": word_manifold}
    elif word_manifold_list is not None:
        word_manifold_dict = {}

        for labelled_manifold in word_manifold_list:
            wm = labelled_manifold.get("word_manifold")
            lc = labelled_manifold.get("label")
            if wm is not None and lc is not None:
                word_manifold_dict[lc] = wm

    response_code, response_json = \
        faq_wrapper.faq_train(instance_name,
                              auth_token=auth_token,
                              caller_name=caller_name,
                              weak_match_threshold=weak_match_threshold,
                              immediate_mode=immediate_mode,
                              requested_word_manifold_dict=word_manifold_dict,
                              callback_url=callback_url)

    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_get_labels(user, token_info,
                           instance_name):
    """
    Get all the possible class labels.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_get_class_labels(instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_curate(user, token_info,
                       instance_name, label_pair):
    """
    Get more details of the samples behind specific cells in the confusion matrix.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param label_pair:
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_curate(instance_name,
                               auth_token=auth_token,
                               caller_name=caller_name,
                               matrix_name=label_pair.get("matrix_name"),
                               true_label=label_pair.get("true_label"),
                               predicted_label=label_pair.get("predicted_label"))
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_tsne_post(user, token_info,
                          instance_name,
                          tsne_settings):
    """
    Run TSNE dimensionality reduction and return the results.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param tsne_settings: Required tsne_settings param.
    :return:
    """
    n_components = tsne_settings.get('n_components')
    perplexity = tsne_settings.get('perplexity')
    learning_rate = tsne_settings.get('learning_rate')
    callback_url = tsne_settings.get("callback_url")

    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_tsne_post(instance_name,
                                                             auth_token=auth_token,
                                                             caller_name=caller_name,
                                                             n_components=n_components,
                                                             perplexity=perplexity,
                                                             learning_rate=learning_rate,
                                                             callback_url=callback_url)

    return response_json, response_code


def faq_matcher_tsne_get(user, token_info,
                         instance_name):
    """
    Run TSNE dimensionality reduction and return the results.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = faq_wrapper.faq_tsne_get(instance_name,
                                                            auth_token=auth_token,
                                                            caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_set_params(user, token_info,
                           instance_name, model_params):
    """
    Modify the models' (hyper) parameters.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param model_params:
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    param_dict = {}

    for attribute, value in model_params.items():
        param_dict[attribute] = value

    response_code, response_json = \
        faq_wrapper.faq_set_params(instance_name,
                                   auth_token=auth_token,
                                   caller_name=caller_name,
                                   param_dict=param_dict)
    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_get_params(user, token_info,
                           instance_name):
    """
    Get the model's (hyper) parameters.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        faq_wrapper.faq_get_params(instance_name,
                                   auth_token=auth_token,
                                   caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def faq_matcher_online_training_samples(user, token_info,
                                        instance_name, labelled_text_sample_list):
    """
    Train the model online/progressively with a few training samples.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_text_sample_list: The training sample(s) to add to the model.
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str]]

    for sample in labelled_text_sample_list:
        lang_code = sample.get("lang_code", "")  # If lang_code isn't given then lang_ident must be run during training
        sample_list.append((sample.get("text"), sample.get("label"), lang_code))

    response_code, response_json = \
        faq_wrapper.faq_add_online_training_samples(iname=instance_name,
                                                    auth_token=auth_token,
                                                    caller_name=caller_name,
                                                    json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"text": result[0], "label": result[1],
                                     "lang_code": result[2],
                                     "uuid": result[3]})

        return result_dict_list, response_code
    else:
        return response_json, response_code
