"""
Wrapper of Feersum_NLU's Image Classifier Python API in HTTP API.
"""
from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
import uuid
from datetime import datetime, timezone
import logging

import requests
# import time

from feersum_nlu.rest_api import wrapper_util, tasks
from feersum_nlu.rest_flask_utils import check_celery_available
from feersum_nlu import engine_utils

from feersum_nlu import image_utils


# ======================== #
# === Start of helpers === #
# ======================== #
def _image_clsfr_cvrt_json_samples_to_2tuples(json_lists) -> List[Tuple[str, str]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[image, label], ...] => List[Tuple[str, str]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[image_str, label_str]]
    """

    # Retrieve samples from json list of lists - [[image, label], ...]
    extracted_tuples = []  # type: List[Tuple[str, str]]

    for json_list in json_lists:
        if (len(json_list) >= 2) and (type(json_list[0]) is str) and \
                (type(json_list[1]) is str):
            extracted_tuples.append((json_list[0], json_list[1]))

    return extracted_tuples


def _image_clsfr_cvrt_json_samples_to_3deltuples(json_lists) -> \
        List[Tuple[Optional[str], Optional[str], Optional[str]]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[image, label, uuid], ...] => List[Tuple[Optional[str], Optional[str],
                                                   Optional[str]]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[Optional[image_str], Optional[label_str], Optional[uuid_str]]]
    """

    # Retrieve samples from json list of lists - [[image, label, uuid], ...]
    extracted_tuples = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str]]]

    for json_list in json_lists:
        if (len(json_list) == 3) and \
                (isinstance(json_list[0], str) or json_list[0] is None) and \
                (isinstance(json_list[1], str) or json_list[1] is None) and \
                (isinstance(json_list[2], str) or json_list[2] is None):

            if ((json_list[0] is not None) and (json_list[1] is not None)) or (json_list[2] is not None):
                # The (image, label) is supplied OR the uuid is supplied.
                extracted_tuples.append((json_list[0], json_list[1], json_list[2]))

    return extracted_tuples


def _image_clsfr_cvrt_json_samples_to_3updtuples(json_lists) -> List[Tuple[str, str, str]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[image, label, uuid], ...] => List[Tuple[str, str, str]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[image_str, label_str, uuid_str]]
    """

    # Retrieve samples from json list of lists - [[image, label, uuid], ...]
    extracted_tuples = []  # type: List[Tuple[str, str, str]]

    for json_list in json_lists:
        if (len(json_list) == 3) and \
                isinstance(json_list[0], str) and \
                isinstance(json_list[1], str) and \
                isinstance(json_list[2], str):
            extracted_tuples.append((json_list[0], json_list[1], json_list[2]))

    return extracted_tuples


def image_clsfr_save_helper(name: str, model_save_mode: wrapper_util.SaveHelperMode,
                            save_in_history: bool = True,
                            save_in_history_message: str = "No additional info.") -> bool:
    """
    Save the meta info and model info + manage local cache.

    Save the meta info and model info + manage cache. Save mode VAPORISE_MODEL used when a new model is created which
    requires the related model in the SDK to be removed. The new model will be added to the SDK during training. Save
    mode SAVE_MODEL is used when the SDK model is added/updated during training. Save mode DONT_SAVE_MODEL is used
    when data stored in the wrapper only is modified and it is unnecessary to modify the related model in the SDK.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param model_save_mode: What to do with related model in the SDK - VAPORISE_MODEL, SAVE_MODEL, DONT_SAVE_MODEL.
    :param save_in_history: Record this revision in the history.
    :param save_in_history_message: The comment to accompany this revision in the history.

    :return: True if success; False otherwise.
    """

    # Save the model first ...
    if model_save_mode == wrapper_util.SaveHelperMode.VAPORISE_MODEL:
        # Permanently deletes the model blob. E.g. when we're creating a new model which stales the model blob.
        wrapper_util.get_vision_engine().vaporise_image_clsfr(name)
    elif model_save_mode == wrapper_util.SaveHelperMode.SAVE_MODEL:
        # Save the model blob.
        success = wrapper_util.get_vision_engine().save_image_clsfr(name)

        if not success:
            return False
    else:
        # Don't save and don't vaporise.
        pass

    # Then save the meta info with updated uuid ...
    meta_info = wrapper_util.image_classifier_dict[name]  # At this point one can assume that the 'name' key exists.

    meta_info.uuid = str(uuid.uuid4())  # Update the uuid of the local copy.

    success = wrapper_util.save_meta_info_blob(name + '.image_clsfr_meta_pickle', meta_info,
                                               save_in_history=save_in_history,
                                               save_in_history_message=save_in_history_message)

    if not success:
        return False

    return True


def image_clsfr_upgrade_meta_info_cm(meta_info_cm):
    upgraded_meta_info = False
    # Upgraded CM should be of type Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]

    for row_label in meta_info_cm.keys():
        for col_label in meta_info_cm[row_label].keys():
            cell_samples = meta_info_cm[row_label][col_label]
            num_samples = len(cell_samples)

            for i in range(num_samples):
                if isinstance(cell_samples[i], str):
                    cell_samples[i] = (cell_samples[i], None)
                    upgraded_meta_info = True

    if upgraded_meta_info:
        logging.debug(f"    image_classifier_wrapper.image_clsfr_upgrade_meta_info_cm: Upgrading samples' meta_info.")

    return upgraded_meta_info


def image_clsfr_upgrade_meta_info_samples(meta_info_samples):
    num_samples = len(meta_info_samples)
    upgraded_meta_info = False

    for i in range(num_samples):
        if len(meta_info_samples[i]) != 3:
            meta_info_samples[i] = (meta_info_samples[i][0], meta_info_samples[i][1],
                                    str(uuid.uuid4()))
            upgraded_meta_info = True

    if upgraded_meta_info:
        logging.debug(f"    image_classifier_wrapper.image_clsfr_upgrade_meta_info_samples: Upgrading samples' meta_info.")

    return upgraded_meta_info


def image_clsfr_upgrade_meta_info(meta_info):
    # Check for older versions of meta_info
    upgrade_meta_info = False

    if hasattr(meta_info, 'validation_confusion_dict') is False:
        upgrade_meta_info = True
        meta_info_validation_confusion_dict = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
    else:
        meta_info_validation_confusion_dict = meta_info.validation_confusion_dict

    if upgrade_meta_info:
        logging.debug(f"    image_classifier_wrapper.image_clsfr_upgrade_meta_info: Upgrading meta_info.")
        meta_info = wrapper_util.ImageClassifierMeta(meta_info.uuid, meta_info.long_name, meta_info.desc,
                                                     meta_info.readonly,
                                                     meta_info.weak_match_threshold,
                                                     meta_info.training_samples,
                                                     meta_info.testing_samples,
                                                     meta_info.training_accuracy,
                                                     meta_info.validation_accuracy,
                                                     meta_info.testing_accuracy,
                                                     meta_info.training_f1,
                                                     meta_info.validation_f1,
                                                     meta_info.testing_f1,
                                                     meta_info.training_confusion_dict,
                                                     meta_info_validation_confusion_dict,
                                                     meta_info.testing_confusion_dict,
                                                     meta_info.confusion_dict_labels,
                                                     meta_info.training_stamp,
                                                     meta_info.clsfr_algorithm)

    # Upgrade older versions of meta_info samples.
    image_clsfr_upgrade_meta_info_samples(meta_info.training_samples)
    image_clsfr_upgrade_meta_info_samples(meta_info.testing_samples)

    # Upgrade older versions of meta_info confusion matrices.
    image_clsfr_upgrade_meta_info_cm(meta_info.training_confusion_dict)
    image_clsfr_upgrade_meta_info_cm(meta_info.validation_confusion_dict)
    image_clsfr_upgrade_meta_info_cm(meta_info.testing_confusion_dict)

    return meta_info


def image_clsfr_load_history_helper(name: str,
                                    revision_uuid: str) -> bool:
    """
    Load the meta info and model info + manage local cache.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param revision_uuid: The uuid of the model revision to attempt to load.
    :return: True if success; False otherwise.
    """

    # Load the meta info first ...
    meta_info = wrapper_util.load_meta_info_blob_from_history(revision_uuid)

    if meta_info is None:
        # Model not available so delete local meta info and model cache and return failure.
        logging.error(f"image_clsfr_load_history_helper: Model history meta_info for {name} is not available!")
        image_clsfr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.ImageClassifierMeta):
        logging.error("image_clsfr_load_history_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the model.
    if wrapper_util.image_classifier_dict.get(name) is not meta_info:
        meta_info = image_clsfr_upgrade_meta_info(meta_info)
        wrapper_util.image_classifier_dict[name] = meta_info

        # Note: If a revision was retrieved from history then the model needs to be RETRAINED! So trash the cached model.
        wrapper_util.get_vision_engine().trash_image_clsfr(name, trash_cache_only=True)

        success = wrapper_util.save_meta_info_blob(name + '.image_clsfr_meta_pickle', meta_info,
                                                   save_in_history=True,
                                                   save_in_history_message=f"Restored {meta_info.uuid}.")
        return success

    return True


def image_clsfr_load_helper(name: str,
                            look_in_trash: bool) -> bool:
    """
    Load the meta info and model info + manage local cache.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param look_in_trash: Will load the model even if the trashed flag in the meta info is True.
    :return: True if success; False otherwise.
    """

    # Load the meta info first ...
    meta_info = wrapper_util.load_meta_info_blob(name=name + '.image_clsfr_meta_pickle',
                                                 look_in_trash=look_in_trash,
                                                 cached_meta_blob=wrapper_util.image_classifier_dict.get(name))

    if meta_info is None:
        # Model not available so delete local meta info and model cache and return failure.
        image_clsfr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.ImageClassifierMeta):
        logging.error("image_clsfr_load_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # Then try and load the model ...
    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the model.
    if wrapper_util.image_classifier_dict.get(name) is not meta_info:
        meta_info = image_clsfr_upgrade_meta_info(meta_info)
        wrapper_util.image_classifier_dict[name] = meta_info

        # Try to load the model which becomes available post training.
        wrapper_util.get_vision_engine().load_image_clsfr(name)

    return True


def image_clsfr_trash_helper(name: str, trash_cache_only: bool = False) -> bool:
    """ Trash the meta info and model info + manage cache. """

    if wrapper_util.image_classifier_dict.get(name) is not None:
        del wrapper_util.image_classifier_dict[name]

    if not trash_cache_only:
        wrapper_util.trash_meta_info_blob(name + '.image_clsfr_meta_pickle')

    wrapper_util.get_vision_engine().trash_image_clsfr(name, trash_cache_only=trash_cache_only)

    return True


def image_clsfr_vaporise_helper(name: str) -> bool:
    """ Vaporise the meta info and model info + manage cache. """

    if wrapper_util.image_classifier_dict.get(name) is not None:
        del wrapper_util.image_classifier_dict[name]

    wrapper_util.vaporise_meta_info_blob(name + '.image_clsfr_meta_pickle')

    wrapper_util.get_vision_engine().vaporise_image_clsfr(name)

    return True


# ======================== #
# ======================== #
# ======================== #


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_create(iname: str,
                       auth_token: str, caller_name: Optional[str],
                       long_name: Optional[str],
                       description: Optional[str],
                       load_from_store: bool,
                       revision_uuid: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None or iname == "":
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    if (load_from_store is True) or (revision_uuid is not None):
        # Load the meta_info blob and the model blob into memory.
        if revision_uuid is not None:
            success = image_clsfr_load_history_helper(name, revision_uuid)
        else:
            success = image_clsfr_load_helper(name, look_in_trash=True)

        meta_info = wrapper_util.image_classifier_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Loading from store failed!"}

        smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.training_confusion_dict)

        smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.validation_confusion_dict)

        smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.testing_confusion_dict)

        return 200, {"name": iname,
                     "id": meta_info.uuid,
                     "long_name": meta_info.long_name,
                     "desc": meta_info.desc,
                     "readonly": meta_info.readonly,
                     "threshold": meta_info.weak_match_threshold,
                     "training_accuracy": meta_info.training_accuracy,
                     "training_f1": meta_info.training_f1,
                     "training_cm": smpl_training_confusion_dict,
                     "validation_accuracy": meta_info.validation_accuracy,
                     "validation_f1": meta_info.validation_f1,
                     "validation_cm": smpl_validation_confusion_dict,
                     "testing_accuracy": meta_info.testing_accuracy,
                     "testing_f1": meta_info.testing_f1,
                     "testing_cm": smpl_testing_confusion_dict,
                     "cm_labels": meta_info.confusion_dict_labels,
                     "training_stamp": meta_info.training_stamp,
                     "num_training_samples": len(meta_info.training_samples),
                     "num_testing_samples": len(meta_info.testing_samples)}
    else:
        # === See if there already exists a model with the same name ===
        success = image_clsfr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.image_classifier_dict.get(name)

        if success and meta_info is not None:
            # The model already exists; check if it is readonly before creating a new one with the same name.
            if meta_info.readonly:
                return 400, {"error_detail": "Named instance {} exists and is readonly!".format(iname)}  # Bad request.
        # === ===

        # Create a new model
        wrapper_util.image_classifier_dict[name] = wrapper_util.ImageClassifierMeta("",
                                                                                    long_name,
                                                                                    description,
                                                                                    False,
                                                                                    1.0,
                                                                                    [], [],
                                                                                    -1.0, -1.0, -1.0,
                                                                                    0.0, 0.0, 0.0,
                                                                                    _training_confusion_dict={},
                                                                                    _validation_confusion_dict={},
                                                                                    _testing_confusion_dict={},
                                                                                    _confusion_dict_labels={},
                                                                                    _training_stamp="",
                                                                                    _clsfr_algorithm="")

        #####

        # Save the named meta_info blob, but permanently delete potentially stale model blob. MIGHT modify the meta info
        image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.VAPORISE_MODEL,
                                save_in_history=True,
                                save_in_history_message="Created model.")

        meta_info = wrapper_util.image_classifier_dict[name]

        return 200, {"name": iname,
                     "id": meta_info.uuid,
                     "long_name": meta_info.long_name,
                     "desc": meta_info.desc,
                     "readonly": meta_info.readonly,
                     "threshold": meta_info.weak_match_threshold,
                     "training_accuracy": meta_info.training_accuracy,
                     "validation_accuracy": meta_info.validation_accuracy,
                     "testing_accuracy": meta_info.testing_accuracy,
                     "training_f1": meta_info.training_f1,
                     "validation_f1": meta_info.validation_f1,
                     "testing_f1": meta_info.testing_f1,
                     "training_cm": {},
                     "validation_cm": {},
                     "testing_cm": {},
                     "cm_labels": {},
                     "training_stamp": meta_info.training_stamp,
                     "num_training_samples": len(meta_info.training_samples),
                     "num_testing_samples": len(meta_info.testing_samples)}


#########################
#########################
#########################
#########################


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_del(iname: str, auth_token: str, caller_name: Optional[str],
                    vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the image classifier model. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory ONLY to return the details.
    if not vaporise:
        success = image_clsfr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.image_classifier_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s
    else:
        success = image_clsfr_load_helper(name, look_in_trash=True)
        meta_info = wrapper_util.image_classifier_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded and not in trash!".format(iname)}

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.testing_confusion_dict)

    # Details of model stored in wrapper.
    details = {"name": name[:-(len(auth_token) + 1)],
               "id": meta_info.uuid,
               "long_name": meta_info.long_name,
               "desc": meta_info.desc,
               "readonly": meta_info.readonly,
               "threshold": meta_info.weak_match_threshold,
               "training_accuracy": meta_info.training_accuracy,
               "validation_accuracy": meta_info.validation_accuracy,
               "testing_accuracy": meta_info.testing_accuracy,
               "training_f1": meta_info.training_f1,
               "validation_f1": meta_info.validation_f1,
               "testing_f1": meta_info.testing_f1,
               "training_cm": smpl_training_confusion_dict,
               "validation_cm": smpl_validation_confusion_dict,
               "testing_cm": smpl_testing_confusion_dict,
               "cm_labels": meta_info.confusion_dict_labels,
               "training_stamp": meta_info.training_stamp,
               "num_training_samples": len(meta_info.training_samples),
               "num_testing_samples": len(meta_info.testing_samples)}

    if not vaporise:
        image_clsfr_trash_helper(name)
    else:
        image_clsfr_vaporise_helper(name)

    return 200, details


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_details(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.testing_confusion_dict)

    # Details of classifier stored in wrapper.
    details = {"name": iname,
               "id": meta_info.uuid,
               "long_name": meta_info.long_name,
               "desc": meta_info.desc,
               "readonly": meta_info.readonly,
               "threshold": meta_info.weak_match_threshold,
               "training_accuracy": meta_info.training_accuracy,
               "validation_accuracy": meta_info.validation_accuracy,
               "testing_accuracy": meta_info.testing_accuracy,
               "training_f1": meta_info.training_f1,
               "validation_f1": meta_info.validation_f1,
               "testing_f1": meta_info.testing_f1,
               "training_cm": smpl_training_confusion_dict,
               "validation_cm": smpl_validation_confusion_dict,
               "testing_cm": smpl_testing_confusion_dict,
               "cm_labels": meta_info.confusion_dict_labels,
               "training_stamp": meta_info.training_stamp,
               "num_training_samples": len(meta_info.training_samples),
               "num_testing_samples": len(meta_info.testing_samples)}

    return 200, details


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_details_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    details_list = []  # type: List[Dict]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.faq_matcher_meta_pickle'

        if name.endswith('.image_clsfr_meta_pickle'):
            meta_info = model_info[1]  # type: wrapper_util.ImageClassifierMeta

            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

            smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
                meta_info.training_confusion_dict)

            smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
                meta_info.validation_confusion_dict if hasattr(meta_info, 'validation_confusion_dict') else {})

            smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
                meta_info.testing_confusion_dict)

            # Details of classifier stored in wrapper.
            details_list.append({"name": name_sans_auth_token_sans_ext,
                                 "id": meta_info.uuid,
                                 "long_name": meta_info.long_name,
                                 "desc": meta_info.desc,
                                 "readonly": meta_info.readonly,
                                 "threshold": meta_info.weak_match_threshold,
                                 "training_accuracy": meta_info.training_accuracy,
                                 "validation_accuracy": meta_info.validation_accuracy,
                                 "testing_accuracy": meta_info.testing_accuracy,
                                 "training_f1": meta_info.training_f1,
                                 "validation_f1": meta_info.validation_f1,
                                 "testing_f1": meta_info.testing_f1,
                                 "training_cm": smpl_training_confusion_dict,
                                 "validation_cm": smpl_validation_confusion_dict,
                                 "testing_cm": smpl_testing_confusion_dict,
                                 "cm_labels": meta_info.confusion_dict_labels,
                                 "training_stamp": meta_info.training_stamp,
                                 "num_training_samples": len(meta_info.training_samples),
                                 "num_testing_samples": len(meta_info.testing_samples)})

    return 200, details_list


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_class_labels(iname: str, auth_token: str,
                                 caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    class_label_list = wrapper_util.get_vision_engine().get_image_clsfr_labels(name)

    if class_label_list is None:
        return 500, {"error_detail": "Class labels for {} not found!".format(iname)}  # Bad/Malformed request.

    return 200, class_label_list


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_set_params(iname: str, auth_token: str, caller_name: Optional[str],
                           param_dict: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    long_name = param_dict.get('long_name')
    desc = param_dict.get('desc')
    readonly = param_dict.get('readonly')
    threshold = param_dict.get('threshold')

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly and (readonly is None or readonly is True):
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if long_name is not None:
        meta_info.long_name = long_name
    if desc is not None:
        meta_info.desc = desc
    if readonly is not None:
        meta_info.readonly = readonly
    if threshold is not None:
        meta_info.weak_match_threshold = threshold

    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Updated parameters.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.image_classifier_dict[name].training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.image_classifier_dict[name].validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.image_classifier_dict[name].testing_confusion_dict)

    meta_info = wrapper_util.image_classifier_dict[name]

    return 200, {"name": iname,
                 "id": meta_info.uuid,
                 "long_name": meta_info.long_name,
                 "desc": meta_info.desc,
                 "readonly": meta_info.readonly,
                 "threshold": meta_info.weak_match_threshold,
                 "training_accuracy": meta_info.training_accuracy,
                 "training_f1": meta_info.training_f1,
                 "training_cm": smpl_training_confusion_dict,
                 "validation_accuracy": meta_info.validation_accuracy,
                 "validation_f1": meta_info.validation_f1,
                 "validation_cm": smpl_validation_confusion_dict,
                 "testing_accuracy": meta_info.testing_accuracy,
                 "testing_f1": meta_info.testing_f1,
                 "testing_cm": smpl_testing_confusion_dict,
                 "cm_labels": meta_info.confusion_dict_labels,
                 "training_stamp": meta_info.training_stamp,
                 "num_training_samples": len(meta_info.training_samples),
                 "num_testing_samples": len(meta_info.testing_samples),
                 "lid_model_file": "lid_za"}


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_params(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    return 200, {"long_name": meta_info.long_name,
                 "desc": meta_info.desc,
                 "readonly": meta_info.readonly,
                 "threshold": meta_info.weak_match_threshold}


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_add_training_samples(iname: str,
                                     auth_token: str, caller_name: Optional[str],
                                     json_training_data: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_training_data is None:
        return 400, {"error_detail": "No training data provided!"}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_training_data is not None:
        json_training_samples = json_training_data.get("samples")
    else:
        json_training_samples = None

    if json_training_samples is None:
        return 400, {"error_detail": "No training samples provided!"}  # Bad/Malformed request.s

    # Retrieve samples from json dict -   # image, label.
    extracted_training_tuples = _image_clsfr_cvrt_json_samples_to_2tuples(json_training_samples)

    if len(extracted_training_tuples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str]]

    format_ok = True

    # Add training samples to meta info avoiding duplicates.
    for image, label in extracted_training_tuples:
        format_ok = image_utils.check_image_format(image)
        if format_ok is False:
            break

        sample_is_duplicate = False

        # Linear search over samples to find the one to update. OK for now.
        for model_sample in meta_info.training_samples:
            if (label == model_sample[1]) and (image == model_sample[0]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.training_samples.append((image, label, str(uuid.uuid4())))
            updated_samples.append(meta_info.training_samples[-1])

    if format_ok is False:
        return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Added training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_training_samples(iname: str, auth_token: str,
                                     index: Optional[int],
                                     length: Optional[int],
                                     caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if index is None:
        index = 0

    if length is None:
        length = len(meta_info.training_samples)

    start = min(max(0, index), len(meta_info.training_samples) - 1)
    end_op = min(max(start, index + length), len(meta_info.training_samples))

    return 200, meta_info.training_samples[start: end_op]


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_remove_training_samples(iname: str,
                                        auth_token: str, caller_name: Optional[str],
                                        json_training_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_training_data None then remove ALL the samples !!!

    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_training_data is not None:
        json_training_samples = json_training_data.get("samples")
    else:
        json_training_samples = None

    if json_training_samples is not None:
        # Remove the extracted_tuples_to_delete from meta_info.training_samples
        extracted_tuples_to_delete = _image_clsfr_cvrt_json_samples_to_3deltuples(json_training_samples)
        removed_samples = []  # type: List[Tuple[str, str, str]]

        for extracted_tuple in extracted_tuples_to_delete:
            num_samples = len(meta_info.training_samples)

            # Linear search over samples to find the one to delete. OK for now.
            for i in range(num_samples):
                sample = meta_info.training_samples[i]
                delete_sample = False

                if extracted_tuple[2] is not None:
                    # Check if sample matches based on uuid.
                    if extracted_tuple[2] == sample[2]:
                        delete_sample = True
                elif (extracted_tuple[0] is not None) and (extracted_tuple[1] is not None):
                    # Check if sample matches based on (image, label).
                    if (extracted_tuple[1] == sample[1]) and (extracted_tuple[0] == sample[0]):
                        delete_sample = True

                if delete_sample:
                    # Delete the matched sample from the meta info list.
                    del meta_info.training_samples[i]
                    removed_samples.append(sample)
                    break  # from for over samples.
    else:
        # No samples provided so clear meta_info.training_samples.
        removed_samples = meta_info.training_samples
        meta_info.training_samples = []

    #  Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                            save_in_history=True,
                            save_in_history_message="Removed training samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_update_training_samples(iname: str,
                                        auth_token: str, caller_name: Optional[str],
                                        json_training_data: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_training_data is None:
        return 400, {"error_detail": "No training data provided!"}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_training_data is not None:
        json_training_samples = json_training_data.get("samples")
    else:
        json_training_samples = None

    if json_training_samples is None:
        return 400, {"error_detail": "No training samples provided!"}  # Bad/Malformed request.s

    # Retrieve samples from json dict -   # image, label.
    extracted_tuples_to_update = _image_clsfr_cvrt_json_samples_to_3updtuples(json_training_samples)

    if len(extracted_tuples_to_update) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str]]

    format_ok = True

    for extracted_tuple in extracted_tuples_to_update:
        num_samples = len(meta_info.training_samples)

        format_ok = image_utils.check_image_format(extracted_tuple[0])
        if format_ok is False:
            break

        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if extracted_tuple[2] == meta_info.training_samples[i][2]:
                # The sample matches based on uuid so update it.
                meta_info.training_samples[i] = extracted_tuple
                updated_samples.append(extracted_tuple)
                break  # from for loop over model's samples.

    if format_ok is False:
        return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Updated training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_add_testing_samples(iname: str,
                                    auth_token: str, caller_name: Optional[str],
                                    json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_testing_data is None:
        return 400, {"error_detail": "No testing data provided!"}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_testing_data is not None:
        json_testing_samples = json_testing_data.get("samples")
    else:
        json_testing_samples = None

    if json_testing_samples is None:
        return 400, {"error_detail": "No testing samples provided!"}  # Bad/Malformed request.

    # Retrieve samples from json dict -   # image, label.
    extracted_testing_tuples = _image_clsfr_cvrt_json_samples_to_2tuples(json_testing_samples)

    if len(extracted_testing_tuples) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str]]

    format_ok = True

    # Add testing samples to meta info avoiding duplicates.
    for image, label in extracted_testing_tuples:
        format_ok = image_utils.check_image_format(image)
        if format_ok is False:
            break

        sample_is_duplicate = False

        for model_sample in meta_info.testing_samples:
            if (label == model_sample[1]) and (image == model_sample[0]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.testing_samples.append((image, label, str(uuid.uuid4())))
            updated_samples.append(meta_info.testing_samples[-1])

    if format_ok is False:
        return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Added testing samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_get_testing_samples(iname: str, auth_token: str,
                                    index: Optional[int],
                                    length: Optional[int],
                                    caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if index is None:
        index = 0

    if length is None:
        length = len(meta_info.testing_samples)

    start = min(max(0, index), len(meta_info.testing_samples) - 1)
    end_op = min(max(start, index + length), len(meta_info.testing_samples))

    return 200, meta_info.testing_samples[start: end_op]


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_remove_testing_samples(iname: str,
                                       auth_token: str, caller_name: Optional[str],
                                       json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_testing_data None then remove ALL the samples !!!

    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_testing_data is not None:
        json_testing_samples = json_testing_data.get("samples")
    else:
        json_testing_samples = None

    if json_testing_samples is not None:
        # Remove the extracted_tuples_to_delete from meta_info.testing_samples
        extracted_tuples_to_delete = _image_clsfr_cvrt_json_samples_to_3deltuples(json_testing_samples)
        removed_samples = []  # type: List[Tuple[str, str, str]]

        for extracted_tuple in extracted_tuples_to_delete:
            num_samples = len(meta_info.testing_samples)

            # Linear search over samples to find the one to delete. OK for now.
            for i in range(num_samples):
                sample = meta_info.testing_samples[i]
                delete_sample = False

                if extracted_tuple[2] is not None:
                    # Check if sample matches based on uuid.
                    if extracted_tuple[2] == sample[2]:
                        delete_sample = True
                elif (extracted_tuple[0] is not None) and (extracted_tuple[1] is not None):
                    # Check if sample matches based on (image, label).
                    if (extracted_tuple[1] == sample[1]) and (extracted_tuple[0] == sample[0]):
                        delete_sample = True

                if delete_sample:
                    # Delete the matched sample from the meta info list.
                    del meta_info.testing_samples[i]
                    removed_samples.append(sample)
                    break  # from for over samples.
    else:
        # No samples provided so clear meta_info.testing_samples.
        removed_samples = meta_info.testing_samples
        meta_info.testing_samples = []

    #  Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                            save_in_history=True,
                            save_in_history_message="Removed testing samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_update_testing_samples(iname: str,
                                       auth_token: str, caller_name: Optional[str],
                                       json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_testing_data is None:
        return 400, {"error_detail": "No testing data provided!"}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_testing_data is not None:
        json_testing_samples = json_testing_data.get("samples")
    else:
        json_testing_samples = None

    if json_testing_samples is None:
        return 400, {"error_detail": "No testing samples provided!"}  # Bad/Malformed request.

    # Retrieve samples from json dict -   # image, label.
    extracted_tuples_to_update = _image_clsfr_cvrt_json_samples_to_3updtuples(json_testing_samples)

    if len(extracted_tuples_to_update) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str]]

    format_ok = True

    for extracted_tuple in extracted_tuples_to_update:
        num_samples = len(meta_info.testing_samples)

        format_ok = image_utils.check_image_format(extracted_tuple[0])
        if format_ok is False:
            break

        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if extracted_tuple[2] == meta_info.testing_samples[i][2]:
                # The sample matches based on uuid so update it.
                meta_info.testing_samples[i] = extracted_tuple
                updated_samples.append(extracted_tuple)
                break  # from for loop over model's samples.

    if format_ok is False:
        return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Updated testing samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


def _image_clsfr_train_impl(iname: str, auth_token: str,
                            weak_match_threshold: Optional[float],
                            clsfr_algorithm: Optional[str],
                            num_epochs: Optional[int],
                            callback_url: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    """
    The training code. This code may be run in a celery process.

    :param iname: The instance name.
    :param auth_token: The auth token used in this call.
    :param weak_match_threshold: The weak match threshold to use during inference.
    :param clsfr_algorithm: The name of the algorithm that should be used for the classification.
    :param num_epochs: The number of epochs to train the model for.
    :param callback_url: The url to send the post train request to.
    :return: The response status and json payload.
    """

    logging.info(f"image_classifier_wrapper._image_clsfr_train_impl: Training task STARTED.")

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (weak_match_threshold is None) or (type(weak_match_threshold) is not float):
        weak_match_threshold = meta_info.weak_match_threshold

    # ===
    # ===

    # === Do the training ===
    success = wrapper_util.get_vision_engine().train_image_clsfr(name,
                                                                 meta_info.training_samples,
                                                                 meta_info.testing_samples,
                                                                 clsfr_algorithm=clsfr_algorithm,
                                                                 num_epochs=num_epochs)

    # validation_accuracy, validation_f1, validation_confusion_dict_full_sl, validation_confusion_dict_labels = \
    #     wrapper_util.get_vision_engine().train_and_cross_validate_image_clsfr(name,
    #                                                                        intent_clsfr_training_expressions,
    #                                                                        intent_clsfr_testing_expressions,,
    #                                                                          word_manifold_dict,
    #                                                                          k=10,
    #                                                                          n_experiments=30)
    # success = len(validation_confusion_dict_labels) > 0
    # === ===

    if not success:
        data = {
            "error_detail": "Training failed! Were training data and valid clsfr_algorithm provided?"
        }

        if callback_url:
            requests.post(callback_url, json=data, timeout=0.0)

        return 400, data

    # HEAVY CPU
    print("Testing the model...", flush=True, end='')
    training_accuracy, training_f1, training_confusion_dict_full_sl, training_confusion_dict_labels = \
        wrapper_util.get_vision_engine().test_image_clsfr(name, meta_info.training_samples,
                                                          weak_match_threshold, 1)
    print("done.")

    # validation_accuracy, validation_f1, validation_confusion_dict_full_sl, validation_confusion_dict_labels = ...
    validation_accuracy = 0.0  # type: float
    validation_f1 = 0.0  # type: float
    validation_confusion_dict_full_sl = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
    validation_confusion_dict_labels = {}  # type: Dict[str, str]

    testing_accuracy, testing_f1, testing_confusion_dict_full_sl, testing_confusion_dict_labels = \
        wrapper_util.get_vision_engine().test_image_clsfr(name, meta_info.testing_samples,
                                                          weak_match_threshold, 1)

    confusion_dict_labels = {**training_confusion_dict_labels,
                             **validation_confusion_dict_labels,
                             **testing_confusion_dict_labels}

    # Update the model meta info.
    meta_info.weak_match_threshold = weak_match_threshold

    meta_info.training_accuracy = training_accuracy
    meta_info.validation_accuracy = validation_accuracy
    meta_info.testing_accuracy = testing_accuracy

    meta_info.training_f1 = training_f1
    meta_info.validation_f1 = validation_f1
    meta_info.testing_f1 = testing_f1

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        training_confusion_dict_full_sl)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        validation_confusion_dict_full_sl)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        testing_confusion_dict_full_sl)

    meta_info.training_confusion_dict = training_confusion_dict_full_sl
    meta_info.validation_confusion_dict = validation_confusion_dict_full_sl
    meta_info.testing_confusion_dict = testing_confusion_dict_full_sl

    meta_info.confusion_dict_labels = confusion_dict_labels

    meta_info.training_stamp = str(datetime.now(timezone.utc).astimezone())
    meta_info.uuid = ""

    wrapper_util.image_classifier_dict[name] = meta_info

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                      save_in_history=True,
                                      save_in_history_message="Trained model.")

    if not success:
        data = {"error_detail": "Saving of model failed!"}

        if callback_url:
            requests.post(callback_url, json=data, timeout=0.0)

        return 500, data

    ############
    ############
    ############

    manifold_name = wrapper_util.image_classifier_dict[name]

    response_data = {
        "name": iname,
        "id": manifold_name.uuid,
        "long_name": manifold_name.long_name,
        "desc": manifold_name.desc,
        "readonly": manifold_name.readonly,
        "threshold": manifold_name.weak_match_threshold,
        "training_accuracy": manifold_name.training_accuracy,
        "training_f1": manifold_name.training_f1,
        "training_cm": smpl_training_confusion_dict,
        "validation_accuracy": manifold_name.validation_accuracy,
        "validation_f1": manifold_name.validation_f1,
        "validation_cm": smpl_validation_confusion_dict,
        "testing_accuracy": manifold_name.testing_accuracy,
        "testing_f1": manifold_name.testing_f1,
        "testing_cm": smpl_testing_confusion_dict,
        "cm_labels": manifold_name.confusion_dict_labels,
        "training_stamp": manifold_name.training_stamp,
        "num_training_samples": len(manifold_name.training_samples),
        "num_testing_samples": len(manifold_name.testing_samples)
    }

    if callback_url:
        requests.post(callback_url, json=response_data, timeout=0.0)

    logging.info(f"image_classifier_wrapper._image_clsfr_train_impl: Training task COMPLETED.")
    return 200, response_data


############
############
############
############


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_train(iname: str, auth_token: str, caller_name: Optional[str],
                      weak_match_threshold: Optional[float],
                      immediate_mode: Optional[bool],
                      clsfr_algorithm: Optional[str],
                      num_epochs: Optional[int],
                      callback_url: Optional[str] = None) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    # ToDo: Force immediate mode to False in production?

    if (immediate_mode is True) or (check_celery_available() is False):
        # Train WITHOUT Celery - synchronously.
        logging.info(f"image_classifier_wrapper.image_clsfr_train: Training synchronously.")
        sync_result = tasks.image_clsfr_train.apply(kwargs={'iname': iname, 'auth_token': auth_token,
                                                            'weak_match_threshold': weak_match_threshold,
                                                            'clsfr_algorithm': clsfr_algorithm,
                                                            'num_epochs': num_epochs,
                                                            'callback_url': None})
        return sync_result.get()  # result is an EagerResult that we know has already been executed.
    else:
        # Train WITH Celery - asynchronously or synchronously if Celery is in eager mode.
        logging.info(f"image_classifier_wrapper.image_clsfr_train: Training synchronously/asynchronously.")
        current_uuid = meta_info.uuid
        async_result = \
            tasks.image_clsfr_train.apply_async(kwargs={'iname': iname, 'auth_token': auth_token,
                                                        'weak_match_threshold': weak_match_threshold,
                                                        'clsfr_algorithm': clsfr_algorithm,
                                                        'num_epochs': num_epochs,
                                                        'callback_url': callback_url})

        if async_result.ready():
            # If it has completed then just return the actual result.
            logging.info(f"image_classifier_wrapper.image_clsfr_train: Training done. Returning sync result in response.")
            return async_result.get()
        else:
            logging.info(f"image_classifier_wrapper.image_clsfr_train: Async training task busy.")
            response_data = {
                "name": iname,
                "id": current_uuid,  # This is the old UUID. The UUID will be updated in the DB when training is done!
                "training_stamp": "ASYNC_TASK - UUID will be updated once done."
            }

            return 200, response_data


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                         image: Optional[str],
                         url: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if (image is None) and (url is None):
        return 400, {"error_detail": "No image provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if image is not None:
        format_ok = image_utils.check_image_format(image)

        if format_ok is False:
            return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s
    elif url is not None:
        try:
            # Get image from url e.g. "https://www.googleapis.com/storage/v1/b/bucket_name/o/blob_name?alt=media"
            response = requests.get(url, timeout=8.0)
            image = image_utils.load_image_from_bytes(response.content)
            format_ok = image_utils.check_image_format(image)  # load_image_from_bytes SHOULD anyway reformat the image.

            if format_ok is False:
                return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.
        except IOError:  # includes requests.exceptions.RequestException & therefore also requests.exceptions.Timeout
            return 400, {"error_detail": f"Couldn't get an image from {url} - IOError or Timeout!"}  # Bad/Malformed request.
    else:
        return 400, {"error_detail": "No image provided!"}  # Bad/Malformed request.

    # # TEST CODE
    # wrapper_util.vision_engine.VisionEngine.save_image("test.jpg", image)

    # [(label, score)]
    scored_label_list = wrapper_util.get_vision_engine().retrieve_image_class(name,
                                                                              image,
                                                                              meta_info.weak_match_threshold,
                                                                              3)

    return 200, scored_label_list


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_curate(iname: str, auth_token: str, caller_name: Optional[str],
                       matrix_name: str, true_label: str, predicted_label: str) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    # ===
    if matrix_name.lower() == 'train':
        confusion_dict = meta_info.training_confusion_dict
    else:
        confusion_dict = meta_info.testing_confusion_dict

    samples = []  # type: List[Dict[str, Optional[str]]]

    dict_row = confusion_dict.get(true_label)
    if dict_row is not None:
        cell = dict_row.get(predicted_label)
        if cell is not None:
            for image, image_uuid in cell:
                samples.append({'image': image, 'label': true_label, 'uuid': image_uuid})

    return 200, samples


@wrapper_util.lock_decorator_vise
@wrapper_util.auth_decorator
def image_clsfr_add_online_training_samples(iname: str,
                                            auth_token: str, caller_name: Optional[str],
                                            json_training_data: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the model blob into memory.
    success = image_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.image_classifier_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_training_data is None:
        return 400, {"error_detail": "No training data provided!"}  # Bad/Malformed request.

    # Extract list of tuples from _samples dict.
    if json_training_data is not None:
        json_training_samples = json_training_data.get("samples")
    else:
        json_training_samples = None

    if json_training_samples is None:
        return 400, {"error_detail": "No training samples provided!"}  # Bad/Malformed request.s

    # Retrieve samples from json dict - image, label
    online_training_tuples = _image_clsfr_cvrt_json_samples_to_2tuples(json_training_samples)

    if len(online_training_tuples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str]]

    format_ok = True

    for image, label in online_training_tuples:
        format_ok = image_utils.check_image_format(image)
        if format_ok is False:
            break

        sample_is_duplicate = False

        for model_sample in meta_info.training_samples:
            if (label == model_sample[1]) and (image == model_sample[0]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.training_samples.append((image, label, str(uuid.uuid4())))
            updated_samples.append(meta_info.training_samples[-1])

    if format_ok is False:
        return 400, {"error_detail": f"Invalid image format."}  # Bad/Malformed request.s

    wrapper_util.image_classifier_dict[name] = meta_info

    success = wrapper_util.get_vision_engine().train_image_clsfr_online(name, online_training_tuples, [])

    if not success:
        return 500, {"error_detail": "Online training failed! Was it trained normally the first time."}

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = image_clsfr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                      save_in_history=False,  # Versioning online samples might create too many revisions!
                                      save_in_history_message="Added online training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples
