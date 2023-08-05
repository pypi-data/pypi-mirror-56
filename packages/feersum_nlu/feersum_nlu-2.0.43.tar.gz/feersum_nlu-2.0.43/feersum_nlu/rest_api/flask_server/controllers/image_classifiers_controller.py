from typing import List, Tuple, Optional  # noqa # pylint: disable=unused-import

import connexion

from feersum_nlu.rest_api.flask_server.controllers import controller_util
from feersum_nlu.rest_api import image_classifier_wrapper


@controller_util.controller_decorator
def image_classifier_add_testing_samples(user, token_info,
                                         instance_name, labelled_image_sample_list):
    """
    Add testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_image_sample_list: ["image":, "label":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str]]

    for sample in labelled_image_sample_list:
        sample_list.append((sample.get("image"), sample.get("label")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_add_testing_samples(iname=instance_name,
                                                                 auth_token=auth_token,
                                                                 caller_name=caller_name,
                                                                 json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_update_testing_samples(user, token_info,
                                            instance_name, labelled_image_sample_list):
    """
    Update testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_image_sample_list: ["image":, "label":]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str]]

    for sample in labelled_image_sample_list:
        sample_list.append((sample.get("image"), sample.get("label"), sample.get("uuid")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_update_testing_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_add_training_samples(user, token_info,
                                          instance_name, labelled_image_sample_list):
    """
    Add testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_image_sample_list: ["image":, "label"::]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str]]

    for sample in labelled_image_sample_list:
        sample_list.append((sample.get("image"), sample.get("label")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_add_training_samples(iname=instance_name,
                                                                  auth_token=auth_token,
                                                                  caller_name=caller_name,
                                                                  json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_update_training_samples(user, token_info,
                                             instance_name, labelled_image_sample_list):
    """
    Update testing samples to the named model.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_image_sample_list: ["image":, "label"::]. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str, str]]

    for sample in labelled_image_sample_list:
        sample_list.append((sample.get("image"), sample.get("label"), sample.get("uuid")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_update_training_samples(iname=instance_name,
                                                                     auth_token=auth_token,
                                                                     caller_name=caller_name,
                                                                     json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_create(user, token_info,
                            create_details):
    """
    Creat a new model or load_from_store i.e. load from the trash!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param create_details: Details like name, long_name and desc.
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    name = create_details.get("name")
    long_name = create_details.get("long_name")
    desc = create_details.get("desc")
    load_from_store = create_details.get("load_from_store")
    revision_uuid = create_details.get("revision_uuid")

    response_code, response_json = image_classifier_wrapper.image_clsfr_create(iname=name,
                                                                               auth_token=auth_token,
                                                                               caller_name=caller_name,
                                                                               long_name=long_name,
                                                                               description=desc,
                                                                               load_from_store=load_from_store,
                                                                               revision_uuid=revision_uuid)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_del(user, token_info,
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

    response_code, response_json = image_classifier_wrapper.image_clsfr_del(instance_name,
                                                                            auth_token=auth_token,
                                                                            caller_name=caller_name,
                                                                            vaporise=False)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_vaporise(user, token_info,
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

    response_code, response_json = image_classifier_wrapper.image_clsfr_del(instance_name,
                                                                            auth_token=auth_token,
                                                                            caller_name=caller_name,
                                                                            vaporise=True)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_del_testing_samples(user, token_info,
                                         instance_name):
    """
    Flask controller endpoint to delete testing samples from an image classifier.

    Flask controller endpoint to delete testing samples from an image classifier. NOTE: The payload of an
    http DEL request is used here!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str]]]

    # Note: The payload of an http DEL request is used here!
    if connexion.request.is_json:
        labelled_image_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in labelled_image_sample_list:
            sample_list.append((sample.get("image"), sample.get("label"),
                                sample.get("uuid")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_remove_testing_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_testing_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_del_testing_samples_all(user, token_info,
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
        image_classifier_wrapper.image_clsfr_remove_testing_samples(iname=instance_name,
                                                                    auth_token=auth_token,
                                                                    caller_name=caller_name,
                                                                    json_testing_data=None)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_del_training_samples(user, token_info,
                                          instance_name):
    """
    Flask controller endpoint to delete testing samples from an image classifier.

    Flask controller endpoint to delete testing samples from an image classifier. NOTE: The payload of an
    http DEL request is used here!

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str]]]

    # Note: The payload of an http DEL request is used here!
    if connexion.request.is_json:
        labelled_image_sample_list = connexion.request.get_json()  # noqa: E501

        for sample in labelled_image_sample_list:
            sample_list.append((sample.get("image"), sample.get("label"),
                                sample.get("uuid")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_remove_training_samples(iname=instance_name,
                                                                     auth_token=auth_token,
                                                                     caller_name=caller_name,
                                                                     json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_del_training_samples_all(user, token_info,
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
        image_classifier_wrapper.image_clsfr_remove_training_samples(iname=instance_name,
                                                                     auth_token=auth_token,
                                                                     caller_name=caller_name,
                                                                     json_training_data=None)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


# ======
# ======
# ======

@controller_util.controller_decorator
def image_classifier_get_details(user, token_info,
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

    response_code, response_json = image_classifier_wrapper.image_clsfr_get_details(instance_name,
                                                                                    auth_token=auth_token,
                                                                                    caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_get_details_all(user, token_info):
    """
    Get details for all your image classifiers.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = image_classifier_wrapper.image_clsfr_get_details_all(auth_token=auth_token,
                                                                                        caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_get_testing_samples(user, token_info,
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
        image_classifier_wrapper.image_clsfr_get_testing_samples(iname=instance_name,
                                                                 auth_token=auth_token,
                                                                 index=index,
                                                                 length=len,
                                                                 caller_name=caller_name)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_get_training_samples(user, token_info,
                                          instance_name,
                                          index=None,
                                          len=None):
    """
    Get the model's training data.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_get_training_samples(iname=instance_name,
                                                                  auth_token=auth_token,
                                                                  index=index,
                                                                  length=len,
                                                                  caller_name=caller_name)

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code


@controller_util.controller_decorator
def image_classifier_retrieve(user, token_info,
                              instance_name, image_input):
    """
    Make a prediction.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param image_input: The base-64 encoded image OR image URL.
    :return: The list of scored labels.
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    image = image_input.get("image")
    url = image_input.get("url")

    response_code, response_json = image_classifier_wrapper.image_clsfr_retrieve(instance_name,
                                                                                 auth_token=auth_token,
                                                                                 caller_name=caller_name,
                                                                                 image=image,
                                                                                 url=url)
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


@controller_util.controller_decorator
def image_classifier_train(user, token_info,
                           instance_name, train_details):
    """
    Train the classifier using the specified algorithm.

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

        clsfr_algorithm = train_details.get("clsfr_algorithm")
        # 'resnet152', etc."

        num_epochs = train_details.get("num_epochs")

        immediate_mode = train_details.get("immediate_mode")
        callback_url = train_details.get("callback_url")
    else:
        weak_match_threshold = None
        clsfr_algorithm = None
        num_epochs = None
        immediate_mode = None
        callback_url = None

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_train(instance_name,
                                                   auth_token=auth_token,
                                                   caller_name=caller_name,
                                                   weak_match_threshold=weak_match_threshold,
                                                   immediate_mode=immediate_mode,
                                                   clsfr_algorithm=clsfr_algorithm,
                                                   num_epochs=num_epochs,
                                                   callback_url=callback_url)

    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_get_labels(user, token_info,
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

    response_code, response_json = image_classifier_wrapper.image_clsfr_get_class_labels(instance_name,
                                                                                         auth_token=auth_token,
                                                                                         caller_name=caller_name)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_curate(user, token_info,
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
        image_classifier_wrapper.image_clsfr_curate(instance_name,
                                                    auth_token=auth_token,
                                                    caller_name=caller_name,
                                                    matrix_name=label_pair.get("matrix_name"),
                                                    true_label=label_pair.get("true_label"),
                                                    predicted_label=label_pair.get("predicted_label"))
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_set_params(user, token_info,
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
        image_classifier_wrapper.image_clsfr_set_params(instance_name,
                                                        auth_token=auth_token,
                                                        caller_name=caller_name,
                                                        param_dict=param_dict)
    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_get_params(user, token_info,
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
        image_classifier_wrapper.image_clsfr_get_params(instance_name,
                                                        auth_token=auth_token,
                                                        caller_name=caller_name)

    return response_json, response_code


@controller_util.controller_decorator
def image_classifier_online_training_samples(user, token_info,
                                             instance_name, labelled_image_sample_list):
    """
    Train the model online/progressively with a few training samples.

    :param user: Basic auth user.
    :param token_info: Basic auth token info.
    :param instance_name: The name of the model. For more info see the swagger spec!
    :param labelled_image_sample_list: The training sample(s) to add to the model.
    :return:
    """
    auth_token = controller_util.get_auth_token()
    caller_name = controller_util.get_caller_name()

    sample_list = []  # type: List[Tuple[str, str]]

    for sample in labelled_image_sample_list:
        sample_list.append((sample.get("image"), sample.get("label")))

    response_code, response_json = \
        image_classifier_wrapper.image_clsfr_add_online_training_samples(iname=instance_name,
                                                                         auth_token=auth_token,
                                                                         caller_name=caller_name,
                                                                         json_training_data={"samples": sample_list})

    if 200 <= response_code <= 299:
        samples_list_list = response_json
        result_dict_list = []

        # Convert from tuple representation to dict representation!
        for result in samples_list_list:
            result_dict_list.append({"image": result[0], "label": result[1],
                                     "uuid": result[2]})

        return result_dict_list, response_code
    else:
        return response_json, response_code
