"""
Wrapper of Feersum_NLU's Text Classifier Python API in HTTP API.
"""
from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
import uuid
from datetime import datetime, timezone
import logging

import random
import requests

from feersum_nlu.rest_api import wrapper_util, tasks
from feersum_nlu.rest_flask_utils import check_celery_available
from feersum_nlu import engine_utils


# ======================== #
# === Start of helpers === #
# ======================== #
def _text_clsfr_cvrt_json_samples_to_3tuples(json_lists) -> List[Tuple[str, str, str]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[text, label, text language hint], ...] => List[Tuple[str, str, str]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[text, label, language hint]]
    """

    # Retrieve samples from json list of lists - [[text, label, text language hint], ...]
    extracted_tuples = []  # type: List[Tuple[str, str, str]]

    for json_list in json_lists:
        if (len(json_list) >= 3) and (type(json_list[0]) is str) and \
                (type(json_list[1]) is str) and (type(json_list[2]) is str):
            extracted_tuples.append((json_list[0], json_list[1], json_list[2]))

    return extracted_tuples


def _text_clsfr_cvrt_json_samples_to_4deltuples(json_lists) -> \
        List[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[text, label, text language hint, uuid], ...] => List[Tuple[Optional[str], Optional[str], Optional[str],
                                                                      Optional[str]]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[Optional[text], Optional[label], Optional[language hint], Optional[uuid_str]]]
    """

    # Retrieve samples from json list of lists - [[text, label, text language hint, uuid], ...]
    extracted_tuples = []  # type: List[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]

    for json_list in json_lists:
        if (len(json_list) == 4) and \
                (isinstance(json_list[0], str) or json_list[0] is None) and \
                (isinstance(json_list[1], str) or json_list[1] is None) and \
                (isinstance(json_list[2], str) or json_list[2] is None) and \
                (isinstance(json_list[3], str) or json_list[3] is None):

            if ((json_list[0] is not None) and (json_list[1] is not None) and (json_list[2] is not None)) or \
                    (json_list[3] is not None):
                # The (text, label, lang_hint) tuple is supplied OR the uuid is supplied.
                extracted_tuples.append((json_list[0], json_list[1], json_list[2], json_list[3]))

    return extracted_tuples


def _text_clsfr_cvrt_json_samples_to_4updtuples(json_lists) -> List[Tuple[str, str, str, str]]:
    """
    Convert a json list of lists sample representation to a list of tuples with some validation.

    Convert a json list of lists sample representation to a list of tuples with some validation.
    i.e. [[text, label, text language hint, uuid], ...] => List[Tuple[str, str, str, str]]

    :param json_lists: The list of list json object to convert to list of tuples.
    :return: List[Tuple[text, label, language hint, uuid_str]]
    """

    # Retrieve samples from json list of lists - [[text, label, text language hint, uuid], ...]
    extracted_tuples = []  # type: List[Tuple[str, str, str, str]]

    for json_list in json_lists:
        if (len(json_list) == 4) and \
                isinstance(json_list[0], str) and \
                isinstance(json_list[1], str) and \
                isinstance(json_list[2], str) and \
                isinstance(json_list[3], str):
            extracted_tuples.append((json_list[0], json_list[1], json_list[2], json_list[3]))

    return extracted_tuples


def text_clsfr_save_helper(name: str, model_save_mode: wrapper_util.SaveHelperMode,
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
        wrapper_util.get_nlpe_engine().vaporise_text_clsfr(name)
    elif model_save_mode == wrapper_util.SaveHelperMode.SAVE_MODEL:
        # Save the model blob.
        success = wrapper_util.get_nlpe_engine().save_text_clsfr(name)

        if not success:
            return False
    else:
        # Don't save and don't vaporise.
        pass

    # Then save the meta info with updated uuid ...
    meta_info = wrapper_util.ntc_dict[name]  # At this point one can assume that the 'name' key exists.

    meta_info.uuid = str(uuid.uuid4())  # Update the uuid of the local copy.

    success = wrapper_util.save_meta_info_blob(name + '.text_clsfr_meta_pickle', meta_info,
                                               save_in_history=save_in_history,
                                               save_in_history_message=save_in_history_message)

    if not success:
        return False

    return True


def text_clsfr_upgrade_meta_info_cm(meta_info_cm):
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
        logging.debug(f"    text_classifier_wrapper.text_clsfr_upgrade_meta_info_cm: Upgrading samples' meta_info.")

    return upgraded_meta_info


def text_clsfr_upgrade_meta_info_samples(meta_info_samples):
    num_samples = len(meta_info_samples)
    upgraded_meta_info = False

    for i in range(num_samples):
        if len(meta_info_samples[i]) != 4:
            meta_info_samples[i] = (meta_info_samples[i][0], meta_info_samples[i][1], meta_info_samples[i][2],
                                    str(uuid.uuid4()))
            upgraded_meta_info = True

    if upgraded_meta_info:
        logging.debug(f"    text_classifier_wrapper.text_clsfr_upgrade_meta_info_samples: Upgrading samples' meta_info.")

    return upgraded_meta_info


def text_clsfr_upgrade_meta_info(meta_info):
    # Check for older versions of meta_info
    upgrade_meta_info = False

    if hasattr(meta_info, 'tsne_results') is False:
        upgrade_meta_info = True
        meta_info_tsne_results = None  # type: Optional[Dict]
    else:
        meta_info_tsne_results = meta_info.tsne_results

    if upgrade_meta_info:
        logging.debug(f"    text_classifier_wrapper.text_clsfr_upgrade_meta_info: Upgrading meta_info.")
        meta_info = wrapper_util.NTCMeta(meta_info.uuid, meta_info.long_name, meta_info.desc,
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
                                         meta_info.validation_confusion_dict,
                                         meta_info.testing_confusion_dict,
                                         meta_info.confusion_dict_labels,
                                         meta_info.training_stamp,
                                         meta_info_tsne_results,
                                         meta_info.clsfr_algorithm,
                                         meta_info.language_model_name_dict)

    # Upgrade older versions of meta_info samples.
    text_clsfr_upgrade_meta_info_samples(meta_info.training_samples)
    text_clsfr_upgrade_meta_info_samples(meta_info.testing_samples)

    # Upgrade older versions of meta_info confusion matrices.
    text_clsfr_upgrade_meta_info_cm(meta_info.training_confusion_dict)
    text_clsfr_upgrade_meta_info_cm(meta_info.validation_confusion_dict)
    text_clsfr_upgrade_meta_info_cm(meta_info.testing_confusion_dict)

    return meta_info


def text_clsfr_load_history_helper(name: str,
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
        logging.error(f"text_clsfr_load_history_helper: Model history meta_info for {name} is not available!")
        text_clsfr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.NTCMeta) or \
            not hasattr(meta_info, 'language_model_name_dict'):  # In case the text classifier is NOT the latest class.
        logging.error("text_clsfr_load_history_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.ntc_dict.get(name) is not meta_info:
        meta_info = text_clsfr_upgrade_meta_info(meta_info)
        wrapper_util.ntc_dict[name] = meta_info

        # Note: If a revision was retrieved from history then the model needs to be RETRAINED! So trash the cached model.
        wrapper_util.get_nlpe_engine().trash_text_clsfr(name, trash_cache_only=True)

        success = wrapper_util.save_meta_info_blob(name + '.text_clsfr_meta_pickle', meta_info,
                                                   save_in_history=True,
                                                   save_in_history_message=f"Restored {meta_info.uuid}.")
        return success

    return True


def text_clsfr_load_helper(name: str,
                           look_in_trash: bool) -> bool:
    """
    Load the meta info and model info + manage local cache.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param look_in_trash: Will load the model even if the trashed flag in the meta info is True.
    :return: True if success; False otherwise.
    """

    # Load the meta info first ...
    meta_info = wrapper_util.load_meta_info_blob(name=name + '.text_clsfr_meta_pickle',
                                                 look_in_trash=look_in_trash,
                                                 cached_meta_blob=wrapper_util.ntc_dict.get(name))

    if meta_info is None:
        # Model not available so delete local meta info and model cache and return failure.
        text_clsfr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.NTCMeta) or \
            not hasattr(meta_info, 'language_model_name_dict'):  # In case the text classifier is NOT the latest class.
        logging.error("text_clsfr_load_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # Then try and load the model ...
    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.ntc_dict.get(name) is not meta_info:
        meta_info = text_clsfr_upgrade_meta_info(meta_info)
        wrapper_util.ntc_dict[name] = meta_info

        # Try to load the model which becomes available post training.
        wrapper_util.get_nlpe_engine().load_text_clsfr(name,
                                                       meta_info.language_model_name_dict)

    return True


def text_clsfr_trash_helper(name: str, trash_cache_only: bool = False) -> bool:
    """ Trash the meta info and model info + manage cache. """

    if wrapper_util.ntc_dict.get(name) is not None:
        del wrapper_util.ntc_dict[name]

    if not trash_cache_only:
        wrapper_util.trash_meta_info_blob(name + '.text_clsfr_meta_pickle')

    wrapper_util.get_nlpe_engine().trash_text_clsfr(name, trash_cache_only=trash_cache_only)

    return True


def text_clsfr_vaporise_helper(name: str) -> bool:
    """ Vaporise the meta info and model info + manage cache. """

    if wrapper_util.ntc_dict.get(name) is not None:
        del wrapper_util.ntc_dict[name]

    wrapper_util.vaporise_meta_info_blob(name + '.text_clsfr_meta_pickle')

    wrapper_util.get_nlpe_engine().vaporise_text_clsfr(name)

    return True


# ======================== #
# ======================== #
# ======================== #


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_create(iname: str,
                      auth_token: str, caller_name: Optional[str],
                      long_name: Optional[str],
                      description: Optional[str],
                      load_from_store: bool,
                      revision_uuid: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None or iname == "":
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    if (load_from_store is True) or (revision_uuid is not None):
        # Load the meta_info blob and the nlpe model blob into memory.
        if revision_uuid is not None:
            success = text_clsfr_load_history_helper(name, revision_uuid)
        else:
            success = text_clsfr_load_helper(name, look_in_trash=True)

        meta_info = wrapper_util.ntc_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Loading from store failed!"}

        smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.training_confusion_dict)

        smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.validation_confusion_dict)

        smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
            meta_info.testing_confusion_dict)

        language_model_list = []  # type: List[Dict[str, str]]
        for lang_code, lang_model in meta_info.language_model_name_dict.items():
            language_model_list.append({'lang_code': lang_code, 'lang_model': lang_model})

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
                     "language_model_list": language_model_list,
                     "lid_model_file": "lid_za"}
    else:
        # === See if there already exists a model with the same name ===
        success = text_clsfr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.ntc_dict.get(name)

        if success and meta_info is not None:
            # The model already exists; check if it is readonly before creating a new one with the same name.
            if meta_info.readonly:
                return 400, {"error_detail": "Named instance {} exists and is readonly!".format(iname)}  # Bad request.
        # === ===

        # Create a new model
        wrapper_util.ntc_dict[name] = wrapper_util.NTCMeta("",
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
                                                           _clsfr_algorithm="",
                                                           _tsne_results=None,
                                                           _language_model_name_dict={}, )

        #####

        # Save the named meta_info blob, but permanently delete potentially stale nlpe model blob. MIGHT modify the meta info
        text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.VAPORISE_MODEL,
                               save_in_history=True,
                               save_in_history_message="Created model.")

        meta_info = wrapper_util.ntc_dict[name]

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
                     "num_testing_samples": len(meta_info.testing_samples),
                     "language_model_list": [],
                     "lid_model_file": "lid_za"}


#########################
#########################
#########################
#########################


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_del(iname: str, auth_token: str, caller_name: Optional[str],
                   vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the text classifier model. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory ONLY to return the details.
    if not vaporise:
        success = text_clsfr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.ntc_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s
    else:
        success = text_clsfr_load_helper(name, look_in_trash=True)
        meta_info = wrapper_util.ntc_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded and not in trash!".format(iname)}

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.testing_confusion_dict)

    language_model_list = []  # type: List[Dict[str, str]]
    for lang_code, lang_model in meta_info.language_model_name_dict.items():
        language_model_list.append({'lang_code': lang_code, 'lang_model': lang_model})

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
               "num_testing_samples": len(meta_info.testing_samples),
               "language_model_list": language_model_list,
               "lid_model_file": "lid_za"}

    if not vaporise:
        text_clsfr_trash_helper(name)
    else:
        text_clsfr_vaporise_helper(name)

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_details(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        meta_info.testing_confusion_dict)

    language_model_list = []  # type: List[Dict[str, str]]
    for lang_code, lang_model in meta_info.language_model_name_dict.items():
        language_model_list.append({'lang_code': lang_code, 'lang_model': lang_model})

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
               "num_testing_samples": len(meta_info.testing_samples),
               "language_model_list": language_model_list,
               "lid_model_file": "lid_za"}

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_details_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    details_list = []  # type: List[Dict]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.faq_matcher_meta_pickle'

        if name.endswith('.text_clsfr_meta_pickle'):
            meta_info = model_info[1]  # type: wrapper_util.NTCMeta

            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

            language_model_list = []  # type: List[Dict[str, str]]
            for lang_code, lang_model in meta_info.language_model_name_dict.items():
                language_model_list.append({'lang_code': lang_code, 'lang_model': lang_model})

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
                                 "num_testing_samples": len(meta_info.testing_samples),
                                 "language_model_list": language_model_list,
                                 "lid_model_file": "lid_za"})

    return 200, details_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_class_labels(iname: str, auth_token: str,
                                caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    class_label_list = wrapper_util.get_nlpe_engine().get_text_clsfr_labels(name)

    if class_label_list is None:
        return 500, {"error_detail": "Class labels for {} not found!".format(iname)}  # Bad/Malformed request.

    return 200, class_label_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_set_params(iname: str, auth_token: str, caller_name: Optional[str],
                          param_dict: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    long_name = param_dict.get('long_name')
    desc = param_dict.get('desc')
    readonly = param_dict.get('readonly')
    threshold = param_dict.get('threshold')

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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

    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                     save_in_history=True,
                                     save_in_history_message="Updated parameters.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    smpl_training_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.ntc_dict[name].training_confusion_dict)

    smpl_validation_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.ntc_dict[name].validation_confusion_dict)

    smpl_testing_confusion_dict = engine_utils.smplfy_confusion_matrix(
        wrapper_util.ntc_dict[name].testing_confusion_dict)

    meta_info = wrapper_util.ntc_dict[name]

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


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_params(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    return 200, {"long_name": meta_info.long_name,
                 "desc": meta_info.desc,
                 "readonly": meta_info.readonly,
                 "threshold": meta_info.weak_match_threshold}


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_add_training_samples(iname: str,
                                    auth_token: str, caller_name: Optional[str],
                                    json_training_data: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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

    # Retrieve samples from json dict -   # text, label, text language hint.
    extracted_training_tuples = _text_clsfr_cvrt_json_samples_to_3tuples(json_training_samples)

    if len(extracted_training_tuples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str, str]]

    # Add training samples to meta info avoiding duplicates.
    for text, label, lang_hint in extracted_training_tuples:
        sample_is_duplicate = False

        # Linear search over samples to find the one to update. OK for now.
        for model_sample in meta_info.training_samples:
            if (text == model_sample[0]) and \
                    (label == model_sample[1]) and \
                    (lang_hint == model_sample[2]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.training_samples.append((text, label, lang_hint, str(uuid.uuid4())))
            updated_samples.append(meta_info.training_samples[-1])

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                     save_in_history=True,
                                     save_in_history_message="Added training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_training_samples(iname: str, auth_token: str,
                                    index: Optional[int],
                                    length: Optional[int],
                                    caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if index is None:
        index = 0

    if length is None:
        length = len(meta_info.training_samples)

    start = min(max(0, index), len(meta_info.training_samples) - 1)
    end_op = min(max(start, index + length), len(meta_info.training_samples))

    return 200, meta_info.training_samples[start: end_op]


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_remove_training_samples(iname: str,
                                       auth_token: str, caller_name: Optional[str],
                                       json_training_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_training_data None then remove ALL the samples !!!

    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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
        extracted_tuples_to_delete = _text_clsfr_cvrt_json_samples_to_4deltuples(json_training_samples)
        removed_samples = []  # type: List[Tuple[str, str, str, str]]

        for extracted_tuple in extracted_tuples_to_delete:
            num_samples = len(meta_info.training_samples)

            # Linear search over samples to find the one to delete. OK for now.
            for i in range(num_samples):
                sample = meta_info.training_samples[i]
                delete_sample = False

                if extracted_tuple[3] is not None:
                    # Check if sample matches based on uuid.
                    if extracted_tuple[3] == sample[3]:
                        delete_sample = True
                elif (extracted_tuple[0] is not None) and (extracted_tuple[1] is not None) and \
                        (extracted_tuple[2] is not None):
                    # Check if sample matches based on (text, label, lang_hint).
                    if (extracted_tuple[1] == sample[1]) and (extracted_tuple[0] == sample[0]) and \
                            (extracted_tuple[2] == sample[2]):
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

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                           save_in_history=True,
                           save_in_history_message="Removed training samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_update_training_samples(iname: str,
                                       auth_token: str, caller_name: Optional[str],
                                       json_training_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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
        return 400, {"error_detail": "No training samples provided!"}  # Bad/Malformed request.

    # Retrieve samples from json dict -   # text, label, text language hint.
    extracted_tuples_to_update = _text_clsfr_cvrt_json_samples_to_4updtuples(json_training_samples)

    if len(extracted_tuples_to_update) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.

    updated_samples = []  # type: List[Tuple[str, str, str, str]]

    for extracted_tuple in extracted_tuples_to_update:
        num_samples = len(meta_info.training_samples)

        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if extracted_tuple[3] == meta_info.training_samples[i][3]:
                # The sample matches based on uuid so update it.
                meta_info.training_samples[i] = extracted_tuple
                updated_samples.append(extracted_tuple)
                break  # from for loop over model's samples.

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                     save_in_history=True,
                                     save_in_history_message="Updated training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_add_testing_samples(iname: str,
                                   auth_token: str, caller_name: Optional[str],
                                   json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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

    # Retrieve samples from json dict -   # text, label, text language hint.
    extracted_testing_tuples = _text_clsfr_cvrt_json_samples_to_3tuples(json_testing_samples)

    if len(extracted_testing_tuples) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str, str]]

    # Add testing samples to meta info avoiding duplicates.
    for text, label, lang_hint in extracted_testing_tuples:
        sample_is_duplicate = False

        for model_sample in meta_info.testing_samples:
            if (text == model_sample[0]) and \
                    (label == model_sample[1]) and \
                    (lang_hint == model_sample[2]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.testing_samples.append((text, label, lang_hint, str(uuid.uuid4())))
            updated_samples.append(meta_info.testing_samples[-1])

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                     save_in_history=True,
                                     save_in_history_message="Added testing samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_get_testing_samples(iname: str, auth_token: str,
                                   index: Optional[int],
                                   length: Optional[int],
                                   caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if index is None:
        index = 0

    if length is None:
        length = len(meta_info.testing_samples)

    start = min(max(0, index), len(meta_info.testing_samples) - 1)
    end_op = min(max(start, index + length), len(meta_info.testing_samples))

    return 200, meta_info.testing_samples[start: end_op]


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_remove_testing_samples(iname: str,
                                      auth_token: str, caller_name: Optional[str],
                                      json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_testing_data None then remove ALL the samples !!!

    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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
        extracted_tuples_to_delete = _text_clsfr_cvrt_json_samples_to_4deltuples(json_testing_samples)
        removed_samples = []  # type: List[Tuple[str, str, str, str]]

        for extracted_tuple in extracted_tuples_to_delete:
            num_samples = len(meta_info.testing_samples)

            # Linear search over samples to find the one to delete. OK for now.
            for i in range(num_samples):
                sample = meta_info.testing_samples[i]
                delete_sample = False

                if extracted_tuple[3] is not None:
                    # Check if sample matches based on uuid.
                    if extracted_tuple[3] == sample[3]:
                        delete_sample = True
                elif (extracted_tuple[0] is not None) and (extracted_tuple[1] is not None) and \
                        (extracted_tuple[2] is not None):
                    # Check if sample matches based on (text, label, lang_hint).
                    if (extracted_tuple[1] == sample[1]) and (extracted_tuple[0] == sample[0]) and \
                            (extracted_tuple[2] == sample[2]):
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

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                           save_in_history=True,
                           save_in_history_message="Removed testing samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_update_testing_samples(iname: str,
                                      auth_token: str, caller_name: Optional[str],
                                      json_testing_data: Optional[Dict]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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

    # Retrieve samples from json dict -   # text, label, text language hint.
    extracted_tuples_to_update = _text_clsfr_cvrt_json_samples_to_4updtuples(json_testing_samples)

    if len(extracted_tuples_to_update) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str, str]]

    for extracted_tuple in extracted_tuples_to_update:
        num_samples = len(meta_info.testing_samples)

        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if extracted_tuple[3] == meta_info.testing_samples[i][3]:
                # The sample matches based on uuid so update it.
                meta_info.testing_samples[i] = extracted_tuple
                updated_samples.append(extracted_tuple)
                break  # from for loop over model's samples.

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                     save_in_history=True,
                                     save_in_history_message="Updated testing samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


def _text_clsfr_train_impl(iname: str, auth_token: str,
                           weak_match_threshold: Optional[float],
                           clsfr_algorithm: Optional[str],
                           requested_language_model_dict: Optional[Dict[str, str]],
                           callback_url: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    """
    The training code. This code may be run in a celery process.

    :param iname: The instance name.
    :param auth_token: The auth token used in this call.
    :param weak_match_threshold: The weak match threshold to use during inference.
    :param clsfr_algorithm: The name of the algorithm that should be used for the classification.
    :param requested_language_model_dict: The names of the language models to use for the lang codes in the associated model.
    :param callback_url: The url to send the post train request to.
    :return: The response status and json payload.
    """

    logging.info(f"text_classifier_wrapper._text_clsfr_train_impl: Training task STARTED.")

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (weak_match_threshold is None) or (type(weak_match_threshold) is not float):
        weak_match_threshold = meta_info.weak_match_threshold

    if requested_language_model_dict is None:
        language_model_dict = {"eng": wrapper_util.nlp_engine.feers_sent_encoder_default}
    else:
        language_model_dict = {}
        for lang_code, lang_model in requested_language_model_dict.items():
            # Use one of the builtin manifolds if requested.
            if lang_model in wrapper_util.nlp_engine.feers_sent_encoder_dict:
                language_model_dict[lang_code] = lang_model
            else:
                language_model_dict[lang_code] = lang_model + "_" + auth_token

    # ===
    # ===

    # === Do the training ===
    success = wrapper_util.get_nlpe_engine().train_text_clsfr(name,
                                                              meta_info.training_samples,
                                                              meta_info.testing_samples,
                                                              clsfr_algorithm=clsfr_algorithm,
                                                              language_model_name_dict=language_model_dict)

    # validation_accuracy, validation_f1, validation_confusion_dict_full_sl, validation_confusion_dict_labels = \
    #     wrapper_util.get_nlpe_engine().train_and_cross_validate_text_clsfr(name,
    #                                                                        intent_clsfr_training_expressions,
    #                                                                        [],
    #                                                                          word_manifold_dict,
    #                                                                          k=10,
    #                                                                          n_experiments=30)
    # success = len(validation_confusion_dict_labels) > 0
    # === ===

    if not success:
        data = {
            "error_detail": "Training failed! Were training data, valid language models and valid clsfr_algorithm provided?"
        }

        if callback_url:
            requests.post(callback_url, json=data, timeout=0.0)

        return 400, data

    # Only test UP TO training_subset_len training samples!
    training_subset_len = 500

    if len(meta_info.training_samples) > training_subset_len:
        training_subset = [meta_info.training_samples[i] for i in
                           random.sample(range(len(meta_info.training_samples)),
                                         training_subset_len)]
    else:
        training_subset = meta_info.training_samples

    # HEAVY CPU
    training_accuracy, training_f1, training_confusion_dict_full_sl, training_confusion_dict_labels = \
        wrapper_util.get_nlpe_engine().test_text_clsfr(name, training_subset,
                                                       weak_match_threshold, 1)

    # validation_accuracy, validation_f1, validation_confusion_dict_full_sl, validation_confusion_dict_labels = ...
    validation_accuracy = 0.0  # type: float
    validation_f1 = 0.0  # type: float
    validation_confusion_dict_full_sl = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
    validation_confusion_dict_labels = {}  # type: Dict[str, str]

    testing_accuracy, testing_f1, testing_confusion_dict_full_sl, testing_confusion_dict_labels = \
        wrapper_util.get_nlpe_engine().test_text_clsfr(name, meta_info.testing_samples,
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

    meta_info.language_model_name_dict = language_model_dict

    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
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

    language_model_list = []  # type: List[Dict[str, str]]
    for lang_code, lang_model in wrapper_util.ntc_dict[name].language_model_name_dict.items():
        language_model_list.append({'lang_code': lang_code, 'lang_model': lang_model})

    manifold_name = wrapper_util.ntc_dict[name]

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
        "num_testing_samples": len(manifold_name.testing_samples),
        "language_model_list": language_model_list,
        "lid_model_file": "lid_za"
    }

    if callback_url:
        requests.post(callback_url, json=response_data, timeout=0.0)

    logging.info(f"text_classifier_wrapper._text_clsfr_train_impl: Training task COMPLETED.")
    return 200, response_data


############
############
############
############


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_train(iname: str, auth_token: str, caller_name: Optional[str],
                     weak_match_threshold: Optional[float],
                     immediate_mode: Optional[bool],
                     clsfr_algorithm: Optional[str],
                     requested_language_model_dict: Optional[Dict[str, str]],
                     callback_url: Optional[str] = None) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    # ToDo: Force immediate mode to False in production?

    if (immediate_mode is True) or (check_celery_available() is False):
        # Train WITHOUT Celery - synchronously.
        logging.info(f"text_classifier_wrapper.text_clsfr_train: Training synchronously.")
        sync_result = tasks.text_clsfr_train.apply(kwargs={'iname': iname, 'auth_token': auth_token,
                                                           'weak_match_threshold': weak_match_threshold,
                                                           'clsfr_algorithm': clsfr_algorithm,
                                                           'requested_language_model_dict': requested_language_model_dict,
                                                           'callback_url': None})
        logging.info(f"text_classifier_wrapper.text_clsfr_train: Training done. Returning sync result in response.")
        return sync_result.get()  # result is an EagerResult that we know has already been executed.
    else:
        # Train WITH Celery - asynchronously or synchronously if Celery is in eager mode.
        logging.info(f"text_classifier_wrapper.text_clsfr_train: Training synchronously/asynchronously.")
        current_uuid = meta_info.uuid
        async_result = \
            tasks.text_clsfr_train.apply_async(kwargs={'iname': iname, 'auth_token': auth_token,
                                                       'weak_match_threshold': weak_match_threshold,
                                                       'clsfr_algorithm': clsfr_algorithm,
                                                       'requested_language_model_dict': requested_language_model_dict,
                                                       'callback_url': callback_url})

        if async_result.ready():
            # If it has completed then just return the actual result.
            logging.info(f"text_classifier_wrapper.text_clsfr_train: Training done. Returning sync result in response.")
            return async_result.get()
        else:
            logging.info(f"text_classifier_wrapper.text_clsfr_train: Async training task busy.")
            response_data = {
                "name": iname,
                "id": current_uuid,  # This is the old UUID. The UUID will be updated in the DB when training is done!
                "training_stamp": "ASYNC_TASK - UUID will be updated once done."
            }

            return 200, response_data


############
############
############
############
############
############


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                        text: Optional[str],
                        lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if text is None:
        return 400, {"error_detail": "No text provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    # [(label, score)], lang_code
    scored_label_list, lang_code = wrapper_util.get_nlpe_engine().retrieve_text_class(name,
                                                                                      text, lang_code,
                                                                                      meta_info.weak_match_threshold,
                                                                                      3)

    return 200, scored_label_list


############
############
############
############
############
############


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_curate(iname: str, auth_token: str, caller_name: Optional[str],
                      matrix_name: str, true_label: str, predicted_label: str) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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
            for text, text_uuid in cell:
                samples.append({'text': text, 'label': true_label, 'uuid': text_uuid})

    return 200, samples


def _text_clsfr_tsne_post_impl(iname: str, auth_token: str,
                               n_components: int, perplexity: float, learning_rate: float,
                               callback_url: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    """
    The training code. This code may be run in a celery process.

    :param iname: The instance name.
    :param auth_token: The auth token used in this call.
    :param callback_url: The url to send the post train request to.
    :return: The response status and json payload.
    """
    logging.info(f"text_classifier_wrapper._text_clsfr_tsne_post_impl: Task STARTED.")

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    tsne_list = wrapper_util.get_nlpe_engine().tsne_text_clsfr(name, n_components, perplexity, learning_rate)

    result_list = []  # type: List[Dict]

    if tsne_list is not None:
        # Convert from tuple representation to dict representation!
        for tsne_tuple in tsne_list:
            result_list.append({"text": tsne_tuple[0], "label": tsne_tuple[1],
                                "x": tsne_tuple[2], "y": tsne_tuple[3], "z": tsne_tuple[4]})

    # Update model's meta info.
    meta_info.tsne_results = {
        "n_components": n_components,
        "perplexity": perplexity,
        "learning_rate": learning_rate,
        "result_list": result_list  # [{"text":,"label":,"x":, "y":, "z":}, ...]
    }

    wrapper_util.ntc_dict[name] = meta_info

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                     save_in_history=False,
                                     save_in_history_message="Updated TSNE results.")

    if not success:
        data = {"error_detail": "Saving of model failed!"}

        if callback_url:
            requests.post(callback_url, json=data, timeout=0.0)

        return 500, data

    ############
    ############
    ############

    if callback_url:
        # Send the complete tsne_results object with the tsne samples as well as the tsne params that were used.
        response_data = {}  # type: wrapper_util.JSONType
        meta_info = wrapper_util.ntc_dict.get(name)
        if (meta_info is not None) and (meta_info.tsne_results is not None):
            response_data = meta_info.tsne_results
        requests.post(callback_url, json=response_data, timeout=0.0)

    logging.info(f"text_classifier_wrapper._text_clsfr_tsne_post_impl: Task COMPLETED.")
    return 200, {}


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_tsne_post(iname: str, auth_token: str, caller_name: Optional[str],
                         n_components: int, perplexity: float, learning_rate: float,
                         callback_url: Optional[str] = None) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if check_celery_available() is False:
        # WITHOUT Celery - synchronously.
        logging.info(f"text_wrapper.text_clsfr_tsne_post: TSNE-ing synchronously.")
        sync_result = tasks.text_clsfr_tsne_post.apply(kwargs={'iname': iname, 'auth_token': auth_token,
                                                               'n_components': n_components, 'perplexity': perplexity,
                                                               'learning_rate': learning_rate,
                                                               'callback_url': None})
        logging.info(f"text_wrapper.text_clsfr_tsne_post: Processing done. Returning sync result in response.")
        return sync_result.get()  # result is an EagerResult that we know has already been executed.
    else:
        # WITH Celery - asynchronously or synchronously if Celery is in eager mode.
        logging.info(f"text_wrapper.text_clsfr_tsne_post: TSNE-ing synchronously/asynchronously.")
        # current_uuid = meta_info.uuid

        async_result = \
            tasks.text_clsfr_tsne_post.apply_async(kwargs={'iname': iname, 'auth_token': auth_token,
                                                           'n_components': n_components, 'perplexity': perplexity,
                                                           'learning_rate': learning_rate,
                                                           'callback_url': callback_url})

        if async_result.ready():
            # If it has completed then just return the actual result.
            logging.info(f"text_wrapper.text_clsfr_tsne_post: Processing done. Returning sync result in response.")
            return async_result.get()
        else:
            logging.info(f"text_wrapper.text_clsfr_tsne_post: Async processing task busy.")
            response_data = {}  # type: wrapper_util.JSONType
            # "name": iname,
            # "id": current_uuid,  # This is the old UUID. The UUID will be updated in the DB when processing is done!

            return 200, response_data


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_tsne_get(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    result_list = []  # type: wrapper_util.JSONType

    if meta_info.tsne_results is not None:
        result_list = meta_info.tsne_results.get('result_list', [])

    return 200, result_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def text_clsfr_add_online_training_samples(iname: str,
                                           auth_token: str, caller_name: Optional[str],
                                           json_training_data: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = text_clsfr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.ntc_dict.get(name)

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

    # Retrieve samples from json dict - text, label, text language hint.
    online_training_tuples = _text_clsfr_cvrt_json_samples_to_3tuples(json_training_samples)

    if len(online_training_tuples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Tuple[str, str, str, str]]

    # Add training data to meta info avoiding duplicates.
    for text, label, lang_hint in online_training_tuples:
        sample_is_duplicate = False

        for model_sample in meta_info.training_samples:
            if (text == model_sample[0]) and (label == model_sample[1]) and (lang_hint == model_sample[2]):
                sample_is_duplicate = True
                break  # break from for-loop

        if not sample_is_duplicate:
            meta_info.training_samples.append((text, label, lang_hint, str(uuid.uuid4())))
            updated_samples.append(meta_info.training_samples[-1])

    wrapper_util.ntc_dict[name] = meta_info

    success = wrapper_util.get_nlpe_engine().train_text_clsfr_online(name, online_training_tuples, [])

    if not success:
        return 500, {"error_detail": "Online training failed! Was it trained normally the first time."}

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = text_clsfr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                     save_in_history=False,  # Versioning online samples might create too many revisions!
                                     save_in_history_message="Added online training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples
