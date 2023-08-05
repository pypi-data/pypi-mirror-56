"""
Wrapper of Feersum_NLU's CRF Entity Extractor Classifier Python API in HTTP API.
"""
from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
import uuid
from datetime import datetime, timezone
import logging

from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import engine_utils


def _validate_json_samples(json_samples: List) -> List:
    """
    Validates json training/testing samples. Returns the valid ones.

    :param json_samples: List of {'text':, 'intent':, 'uuid':, 'entity_list': [{'index':, 'len':, 'entity':}]}.
    :return: Valid json samples.
    """
    valid_crf_samples = []  # type: List[Dict]

    for json_sample in json_samples:
        crf_sample = {'text': json_sample.get('text'),
                      'intent': json_sample.get('intent'),
                      'uuid': json_sample.get('uuid')}

        json_entity_list = json_sample.get('entity_list')

        if isinstance(json_entity_list, list):
            valid_entity_list = []  # type: List[Dict]

            for json_entity in json_entity_list:
                if isinstance(json_entity, dict):
                    entity = json_entity.get('entity')

                    if isinstance(entity, str):
                        if isinstance(json_sample.get('text'), str):
                            # The sample has a text utterance so entities can be specified as (entity,index,len)
                            index = json_entity.get('index')
                            entity_len = json_entity.get('len')

                            if isinstance(index, int) and isinstance(entity_len, int):
                                valid_entity_list.append({'index': index, 'len': entity_len, 'entity': entity})

            crf_sample['entity_list'] = valid_entity_list

        valid_crf_samples.append(crf_sample)

    return valid_crf_samples


def crf_extr_save_helper(name: str, model_save_mode: wrapper_util.SaveHelperMode,
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
        wrapper_util.get_nlpe_engine().vaporise_crf_extr(name)
    elif model_save_mode == wrapper_util.SaveHelperMode.SAVE_MODEL:
        # Save the model blob.
        success = wrapper_util.get_nlpe_engine().save_crf_extr(name)

        if not success:
            return False
    else:
        # Don't save and don't vaporise.
        pass

    # Then save the meta info with updated uuid ...
    meta_info = wrapper_util.crf_extr_dict[name]  # At this point one can assume that the 'name' key exists.

    meta_info.uuid = str(uuid.uuid4())  # Update the uuid of the local copy.

    success = wrapper_util.save_meta_info_blob(name + '.crf_extr_meta_pickle', meta_info,
                                               save_in_history=save_in_history,
                                               save_in_history_message=save_in_history_message)

    if not success:
        return False

    return True


def crf_extr_upgrade_meta_info(meta_info):
    # Check for older versions of meta_info
    return meta_info


def crf_extr_load_history_helper(name: str,
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
        logging.error(f"crf_extr_load_history_helper: Model {name} is not available!")
        crf_extr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.CRFExtractorMeta):
        logging.error("crf_extr_load_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.crf_extr_dict.get(name) is not meta_info:
        meta_info = crf_extr_upgrade_meta_info(meta_info)
        wrapper_util.crf_extr_dict[name] = meta_info

        # Note: If a revision was retrieved from history then the model needs to be RETRAINED! So trash the cached model.
        wrapper_util.get_nlpe_engine().trash_crf_extr(name, trash_cache_only=True)

        success = wrapper_util.save_meta_info_blob(name + '.crf_extr_meta_pickle', meta_info,
                                                   save_in_history=True,
                                                   save_in_history_message=f"Restored {meta_info.uuid}.")
        return success

    return True


def crf_extr_load_helper(name: str,
                         look_in_trash: bool) -> bool:
    """
    Load the meta info and model info + manage local cache.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param look_in_trash: Will load the model even if the trashed flag in the meta info is True.
    :return: True if success; False otherwise.
    """

    meta_info = wrapper_util.load_meta_info_blob(name=name + '.crf_extr_meta_pickle',
                                                 look_in_trash=look_in_trash,
                                                 cached_meta_blob=wrapper_util.crf_extr_dict.get(name))

    if meta_info is None:
        # Model not available so delete local meta info and model cache and return failure.
        crf_extr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.CRFExtractorMeta):
        logging.error("crf_extr_load_helper: Loaded model meta_info object of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # Then try and load the model ...
    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.crf_extr_dict.get(name) is not meta_info:
        meta_info = crf_extr_upgrade_meta_info(meta_info)
        wrapper_util.crf_extr_dict[name] = meta_info

        # Try to load the model which becomes available post training.
        wrapper_util.get_nlpe_engine().load_crf_extr(name)

    return True


def crf_extr_trash_helper(name: str, trash_cache_only: bool = False) -> bool:
    """ Trash the meta info and model info + manage cache. """

    if wrapper_util.crf_extr_dict.get(name) is not None:
        del wrapper_util.crf_extr_dict[name]

    if not trash_cache_only:
        wrapper_util.trash_meta_info_blob(name + '.crf_extr_meta_pickle')

    wrapper_util.get_nlpe_engine().trash_crf_extr(name, trash_cache_only=trash_cache_only)

    return True


def crf_extr_vaporise_helper(name: str) -> bool:
    """ Vaporise the meta info and model info + manage cache. """

    if wrapper_util.crf_extr_dict.get(name) is not None:
        del wrapper_util.crf_extr_dict[name]

    wrapper_util.vaporise_meta_info_blob(name + '.crf_extr_meta_pickle')

    wrapper_util.get_nlpe_engine().vaporise_crf_extr(name)

    return True


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_create(iname: str,
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
            success = crf_extr_load_history_helper(name, revision_uuid)
        else:
            success = crf_extr_load_helper(name, look_in_trash=True)

        meta_info = wrapper_util.crf_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Loading from store failed!"}

        return 200, {"name": iname,
                     "id": meta_info.uuid,
                     "long_name": meta_info.long_name,
                     "desc": meta_info.desc,
                     "readonly": meta_info.readonly,
                     "threshold": meta_info.weak_match_threshold,
                     "training_accuracy": meta_info.training_accuracy,
                     "training_f1": meta_info.training_f1,
                     "validation_accuracy": meta_info.validation_accuracy,
                     "validation_f1": meta_info.validation_f1,
                     "testing_accuracy": meta_info.testing_accuracy,
                     "testing_f1": meta_info.testing_f1,
                     "training_stamp": meta_info.training_stamp,
                     "num_training_samples": len(meta_info.training_samples),
                     "num_testing_samples": len(meta_info.testing_samples)
                     }
    else:
        # === See if there already exists a model with the same name ===
        success = crf_extr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.crf_extr_dict.get(name)

        if success and meta_info is not None:
            # The model already exists; check if it is readonly before creating a new one with the same name.
            if meta_info.readonly:
                return 400, {"error_detail": "Named instance {} exists and is readonly!".format(iname)}  # Bad request.
        # === ===

        # Create a new model
        wrapper_util.crf_extr_dict[name] = wrapper_util.CRFExtractorMeta("",
                                                                         long_name,
                                                                         description,
                                                                         False,
                                                                         1.0,
                                                                         [], [],
                                                                         -1.0, -1.0, -1.0,
                                                                         0.0, 0.0, 0.0,
                                                                         _training_stamp="")

        #####

        # Save the named meta_info blob, but permanently delete potentially stale nlpe model blob. MIGHT modify the meta info
        crf_extr_save_helper(name, wrapper_util.SaveHelperMode.VAPORISE_MODEL,
                             save_in_history=True,
                             save_in_history_message="Created model.")

        return 200, {"name": iname,
                     "id": wrapper_util.crf_extr_dict[name].uuid,
                     "long_name": wrapper_util.crf_extr_dict[name].long_name,
                     "desc": wrapper_util.crf_extr_dict[name].desc,
                     "readonly": wrapper_util.crf_extr_dict[name].readonly,
                     "threshold": wrapper_util.crf_extr_dict[name].weak_match_threshold,
                     "training_accuracy": wrapper_util.crf_extr_dict[name].training_accuracy,
                     "validation_accuracy": wrapper_util.crf_extr_dict[name].validation_accuracy,
                     "testing_accuracy": wrapper_util.crf_extr_dict[name].testing_accuracy,
                     "training_f1": wrapper_util.crf_extr_dict[name].training_f1,
                     "validation_f1": wrapper_util.crf_extr_dict[name].validation_f1,
                     "testing_f1": wrapper_util.crf_extr_dict[name].testing_f1,
                     "training_stamp": wrapper_util.crf_extr_dict[name].training_stamp,
                     "num_training_samples": len(wrapper_util.crf_extr_dict[name].training_samples),
                     "num_testing_samples": len(wrapper_util.crf_extr_dict[name].testing_samples)
                     }


#########################
#########################
#########################
#########################


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_del(iname: str, auth_token: str, caller_name: Optional[str],
                 vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the crf extr model. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    details = {}  # type: Dict

    # Load the meta_info blob and the nlpe model blob into memory ONLY to return the details.
    if not vaporise:
        success = crf_extr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.crf_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s
    else:
        success = crf_extr_load_helper(name, look_in_trash=True)
        meta_info = wrapper_util.crf_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded and not in trash!".format(iname)}

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
               "training_stamp": meta_info.training_stamp,
               "num_training_samples": len(meta_info.training_samples),
               "num_testing_samples": len(meta_info.testing_samples)
               }

    if not vaporise:
        crf_extr_trash_helper(name)
    else:
        crf_extr_vaporise_helper(name)

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_details(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

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
               "training_stamp": meta_info.training_stamp,
               "num_training_samples": len(meta_info.training_samples),
               "num_testing_samples": len(meta_info.testing_samples)
               }

    return 200, details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_details_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    details_list = []  # type: List[Dict]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.faq_matcher_meta_pickle'

        if name.endswith('.crf_extr_meta_pickle'):
            meta_info = model_info[1]  # type: wrapper_util.CRFExtractorMeta

            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

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
                                 "training_stamp": meta_info.training_stamp,
                                 "num_training_samples": len(meta_info.training_samples),
                                 "num_testing_samples": len(meta_info.testing_samples)
                                 })

    return 200, details_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_class_labels(iname: str, auth_token: str,
                              caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    class_label_list = wrapper_util.get_nlpe_engine().get_crf_extr_labels(name)

    if class_label_list is None:
        return 500, {"error_detail": "Class labels for {} not found!".format(iname)}  # Bad/Malformed request.

    return 200, class_label_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_set_params(iname: str, auth_token: str, caller_name: Optional[str],
                        param_dict: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    long_name = param_dict.get('long_name')
    desc = param_dict.get('desc')
    readonly = param_dict.get('readonly')
    threshold = param_dict.get('threshold')

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly and (readonly is None or readonly is True):
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    meta_info = wrapper_util.CRFExtractorMeta(meta_info.uuid,
                                              meta_info.long_name,
                                              meta_info.desc,
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
                                              meta_info.training_stamp)

    if long_name is not None:
        meta_info.long_name = long_name
    if desc is not None:
        meta_info.desc = desc
    if readonly is not None:
        meta_info.readonly = readonly
    if threshold is not None:
        meta_info.weak_match_threshold = threshold

    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                   save_in_history=True,
                                   save_in_history_message="Updated parameters.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, {"name": iname,
                 "id": wrapper_util.crf_extr_dict[name].uuid,
                 "long_name": wrapper_util.crf_extr_dict[name].long_name,
                 "desc": wrapper_util.crf_extr_dict[name].desc,
                 "readonly": wrapper_util.crf_extr_dict[name].readonly,
                 "threshold": wrapper_util.crf_extr_dict[name].weak_match_threshold,
                 "training_accuracy": wrapper_util.crf_extr_dict[name].training_accuracy,
                 "training_f1": wrapper_util.crf_extr_dict[name].training_f1,
                 "validation_accuracy": wrapper_util.crf_extr_dict[name].validation_accuracy,
                 "validation_f1": wrapper_util.crf_extr_dict[name].validation_f1,
                 "testing_accuracy": wrapper_util.crf_extr_dict[name].testing_accuracy,
                 "testing_f1": wrapper_util.crf_extr_dict[name].testing_f1,
                 "training_stamp": wrapper_util.crf_extr_dict[name].training_stamp,
                 "num_training_samples": len(wrapper_util.crf_extr_dict[name].training_samples),
                 "num_testing_samples": len(wrapper_util.crf_extr_dict[name].testing_samples)
                 }


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_params(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    return 200, {"long_name": meta_info.long_name,
                 "desc": meta_info.desc,
                 "readonly": meta_info.readonly,
                 "threshold": meta_info.weak_match_threshold}


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_add_training_samples(iname: str,
                                  auth_token: str, caller_name: Optional[str],
                                  json_training_samples: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (json_training_samples is None) or (len(json_training_samples) == 0):
        return 400, {"error_detail": "No training data provided!"}  # Bad/Malformed request.s

    # Retrieve crf samples from json dict ...
    valid_samples = _validate_json_samples(json_training_samples)

    if len(valid_samples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Dict]

    # Add valid samples if not exact duplicate of samples already added:
    # - Duplicate check is a naive dict comparison.
    # - Improved duplicate checking and sample mergeing would require that one ask the model if samples are duplicates or
    #   to merge samples.
    # A general risk in removing samples here is that it might impact, for example, the balancing of classes.
    for valid_sample in valid_samples:
        is_duplicate = False

        if (valid_sample.get('entity_list') is None) or (valid_sample.get('text') is None):
            return 400, {"error_detail": "All samples must have text and an entity_list!"}  # Bad/Malformed request.s

        # Check if valid_sample already exists in meta_info.training_samples
        for model_sample in meta_info.training_samples:
            if (valid_sample.get('text') == model_sample.get('text')) and \
                    (valid_sample.get('entity_list') == model_sample.get('entity_list')):
                is_duplicate = True
                break  # from for-loop.

        if is_duplicate is False:
            valid_sample['uuid'] = str(uuid.uuid4())
            meta_info.training_samples.append(valid_sample)
            updated_samples.append(valid_sample)

    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                         save_in_history=True,
                         save_in_history_message="Added training samples.")

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_training_samples(iname: str, auth_token: str,
                                  index: Optional[int],
                                  length: Optional[int],
                                  caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

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
def crf_extr_remove_training_samples(iname: str,
                                     auth_token: str, caller_name: Optional[str],
                                     json_samples_to_delete: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_samples_to_delete None then remove ALL the samples !!!
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_samples_to_delete is not None:
        # Remove the extracted_tuples_to_delete from meta_info.training_samples
        valid_samples_to_delete = _validate_json_samples(json_samples_to_delete)

        if len(valid_samples_to_delete) != len(json_samples_to_delete):
            return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

        removed_samples = []

        for sample_to_delete in valid_samples_to_delete:
            num_model_samples = len(meta_info.training_samples)
            for i in range(num_model_samples):
                if sample_to_delete.get('uuid') is not None:
                    if sample_to_delete.get('uuid') == meta_info.training_samples[i].get('uuid'):
                        removed_samples.append(meta_info.training_samples[i])
                        del meta_info.training_samples[i]
                        break
                else:
                    if (sample_to_delete.get('entity_list') is None) or (sample_to_delete.get('text') is None):
                        return 400, {
                            "error_detail": "Samples must have text and an entity_list if uuid not used as reference!"
                        }  # Bad/Malformed request.

                    if (sample_to_delete.get('text') == meta_info.training_samples[i].get('text')) and (
                            sample_to_delete.get('entity_list') == meta_info.training_samples[i].get('entity_list')):
                        removed_samples.append(meta_info.training_samples[i])
                        del meta_info.training_samples[i]
                        break
    else:
        # No samples provided so clear meta_info.training_samples.
        removed_samples = meta_info.training_samples
        meta_info.training_samples = []

    wrapper_util.crf_extr_dict[name] = wrapper_util.CRFExtractorMeta(meta_info.uuid,
                                                                     meta_info.long_name,
                                                                     meta_info.desc,
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
                                                                     meta_info.training_stamp)

    # Save the named meta_info blob. MIGHT modify the meta_info!
    crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                         save_in_history=True,
                         save_in_history_message="Removed training samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_update_training_samples(iname: str,
                                     auth_token: str, caller_name: Optional[str],
                                     json_training_samples: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (json_training_samples is None) or (len(json_training_samples) == 0):
        return 400, {"error_detail": "No training data provided!"}  # Bad/Malformed request.s

    # Retrieve crf samples from json dict ...
    valid_samples = _validate_json_samples(json_training_samples)

    if len(valid_samples) != len(json_training_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Dict]

    for valid_sample in valid_samples:
        num_samples = len(meta_info.training_samples)

        if (valid_sample.get('entity_list') is None) or (valid_sample.get('text') is None):
            return 400, {"error_detail": "All samples must have text and an entity_list!"}  # Bad/Malformed request.s

        # Check if valid_sample already exists in meta_info.training_samples
        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if valid_sample.get('uuid') == meta_info.training_samples[i].get('uuid'):
                # The sample matches based on uuid so update it.
                meta_info.training_samples[i] = valid_sample
                updated_samples.append(valid_sample)
                break  # from for loop over model's samples.

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                   save_in_history=True,
                                   save_in_history_message="Added training samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_add_testing_samples(iname: str,
                                 auth_token: str, caller_name: Optional[str],
                                 json_testing_samples: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (json_testing_samples is None) or (len(json_testing_samples) == 0):
        return 400, {"error_detail": "No testing data provided!"}  # Bad/Malformed request.

    # Retrieve samples from json dict -   # text, label
    valid_samples = _validate_json_samples(json_testing_samples)

    if len(valid_samples) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Dict]

    # Add valid samples if not exact duplicate of samples already added:
    # - Duplicate check is a naive dict comparison.
    # - Improved duplicate checking and sample mergeing would require that one ask the model if samples are duplicates or
    #   to merge samples.
    # A general risk in removing samples here is that it might impact, for example, the balancing of classes.
    for valid_sample in valid_samples:
        is_duplicate = False

        if (valid_sample.get('entity_list') is None) or (valid_sample.get('text') is None):
            return 400, {"error_detail": "All samples must have text and an entity_list!"}  # Bad/Malformed request.s

        # Check if valid_sample already exists in meta_info.training_samples
        for model_sample in meta_info.testing_samples:
            if (valid_sample.get('text') == model_sample.get('text')) and \
                    (valid_sample.get('entity_list') == model_sample.get('entity_list')):
                is_duplicate = True
                break  # from for-loop.

        if is_duplicate is False:
            valid_sample['uuid'] = str(uuid.uuid4())
            meta_info.testing_samples.append(valid_sample)
            updated_samples.append(valid_sample)

    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                         save_in_history=True,
                         save_in_history_message="Added testing samples.")

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_get_testing_samples(iname: str, auth_token: str,
                                 index: Optional[int],
                                 length: Optional[int],
                                 caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

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
def crf_extr_remove_testing_samples(iname: str,
                                    auth_token: str, caller_name: Optional[str],
                                    json_samples_to_delete: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    # if json_samples_to_delete None then remove ALL the samples !!!

    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if json_samples_to_delete is not None:
        # Remove the extracted_tuples_to_delete from meta_info.testing_samples
        valid_samples_to_delete = _validate_json_samples(json_samples_to_delete)

        if len(valid_samples_to_delete) != len(json_samples_to_delete):
            return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

        removed_samples = []

        for sample_to_delete in valid_samples_to_delete:
            num_model_samples = len(meta_info.testing_samples)
            for i in range(num_model_samples):
                if sample_to_delete.get('uuid') is not None:
                    if sample_to_delete.get('uuid') == meta_info.testing_samples[i].get('uuid'):
                        removed_samples.append(meta_info.testing_samples[i])
                        del meta_info.testing_samples[i]
                        break
                else:
                    if (sample_to_delete.get('entity_list') is None) or (sample_to_delete.get('text') is None):
                        return 400, {
                            "error_detail": "Samples must have text and an entity_list if uuid not used as reference!"
                        }  # Bad/Malformed request.

                    if (sample_to_delete.get('text') == meta_info.testing_samples[i].get('text')) and (
                            sample_to_delete.get('entity_list') == meta_info.testing_samples[i].get('entity_list')):
                        removed_samples.append(meta_info.testing_samples[i])
                        del meta_info.testing_samples[i]
                        break
    else:
        # No samples provided so clear meta_info.testing_samples.
        removed_samples = meta_info.testing_samples
        meta_info.testing_samples = []

    wrapper_util.crf_extr_dict[name] = wrapper_util.CRFExtractorMeta(meta_info.uuid,
                                                                     meta_info.long_name,
                                                                     meta_info.desc,
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
                                                                     meta_info.training_stamp)

    # Save the named meta_info blob. MIGHT modify the meta_info!
    crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                         save_in_history=True,
                         save_in_history_message="Removed testing samples.")

    return 200, removed_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_update_testing_samples(iname: str,
                                    auth_token: str, caller_name: Optional[str],
                                    json_testing_samples: Optional[List]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    if (json_testing_samples is None) or (len(json_testing_samples) == 0):
        return 400, {"error_detail": "No testing data provided!"}  # Bad/Malformed request.

    # Retrieve samples from json dict -   # text, label
    valid_samples = _validate_json_samples(json_testing_samples)

    if len(valid_samples) != len(json_testing_samples):
        return 400, {"error_detail": "Not all samples were well formed!"}  # Bad/Malformed request.s

    updated_samples = []  # type: List[Dict]

    for valid_sample in valid_samples:
        num_samples = len(meta_info.testing_samples)

        if (valid_sample.get('entity_list') is None) or (valid_sample.get('text') is None):
            return 400, {"error_detail": "All samples must have text and an entity_list!"}  # Bad/Malformed request.s

        # Check if valid_sample already exists in meta_info.training_samples
        # Linear search over samples to find the one to update. OK for now.
        for i in range(num_samples):
            if valid_sample.get('uuid') == meta_info.testing_samples[i].get('uuid'):
                # The sample matches based on uuid so update it.
                meta_info.testing_samples[i] = valid_sample
                updated_samples.append(valid_sample)
                break  # from for loop over model's samples.

    # ===
    # Make sure dict points to latest instance.
    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = crf_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                   save_in_history=True,
                                   save_in_history_message="Updated testing samples.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, updated_samples


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_train(iname: str, auth_token: str, caller_name: Optional[str],
                   weak_match_threshold: Optional[float]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    if meta_info.readonly:
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    json_samples = []
    json_samples.extend(meta_info.training_samples)
    json_samples.extend(meta_info.testing_samples)

    crf_samples = wrapper_util.get_nlpe_engine().cnvrt_json_to_crf_samples(json_samples)
    crf_training_samples = crf_samples[:len(meta_info.training_samples)]
    crf_testing_samples = crf_samples[len(meta_info.training_samples):]

    if (weak_match_threshold is None) or (type(weak_match_threshold) is not float):
        weak_match_threshold = meta_info.weak_match_threshold

    success = wrapper_util.get_nlpe_engine().train_crf_extr(name,
                                                            crf_training_samples,
                                                            crf_testing_samples)

    if not success:
        return 400, {"error_detail": "Training failed! Was training data provided?"}  # Bad/Malformed request.

    # Only test UP TO training_subset_len training samples!
    # training_subset_len = 500
    #
    # if len(meta_info.training_samples) > training_subset_len:
    #     training_subset = [meta_info.training_samples[i] for i in
    #                        random.sample(range(len(meta_info.training_samples)), training_subset_len)]
    # else:
    #     training_subset = meta_info.training_samples

    # HEAVY CPU
    training_accuracy, training_f1, training_confusion_dict_full_sl, training_confusion_dict_labels = \
        wrapper_util.get_nlpe_engine().test_crf_extr(name, crf_training_samples, 1.0)

    # validation_accuracy, validation_f1, validation_confusion_dict_full_sl, validation_confusion_dict_labels = ...
    validation_accuracy = 0.0  # type: float
    validation_f1 = 0.0  # type: float
    validation_confusion_dict_full_sl = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]
    validation_confusion_dict_labels = {}  # type: Dict[str, str]

    testing_accuracy, testing_f1, testing_confusion_dict_full_sl, testing_confusion_dict_labels = \
        wrapper_util.get_nlpe_engine().test_crf_extr(name, crf_testing_samples, 1.0)

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

    # The below fields are not part of the default extractor meta info & only returned on train operation!
    # meta_info.training_confusion_dict = training_confusion_dict_full_sl
    # meta_info.validation_confusion_dict = validation_confusion_dict_full_sl
    # meta_info.testing_confusion_dict = testing_confusion_dict_full_sl

    # meta_info.confusion_dict_labels = confusion_dict_labels

    meta_info.training_stamp = str(datetime.now(timezone.utc).astimezone())
    meta_info.uuid = ""

    wrapper_util.crf_extr_dict[name] = meta_info

    # Save the named meta_info and model blobs. MIGHT modify the meta_info!
    success = crf_extr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                   save_in_history=True,
                                   save_in_history_message="Trained the model.")

    if not success:
        return 500, {"error_detail": "Saving of model failed!"}

    ############
    ############
    ############

    meta_info = wrapper_util.crf_extr_dict[name]

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
                 "cm_labels": confusion_dict_labels,  # meta_info.confusion_dict_labels,
                 "training_stamp": meta_info.training_stamp,
                 "num_training_samples": len(meta_info.training_samples),
                 "num_testing_samples": len(meta_info.testing_samples)
                 }


############
############
############
############


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def crf_extr_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                      text: Optional[str],
                      lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    if text is None:
        return 400, {"error_detail": "No text provided!"}  # Bad/Malformed request.

    # Truncate the text if env variable configured and >= 0
    if (wrapper_util.entity_retrieve_MAX_TEXT_LENGTH >= 0) and (len(text) > wrapper_util.entity_retrieve_MAX_TEXT_LENGTH):
        text = text[:wrapper_util.entity_retrieve_MAX_TEXT_LENGTH]
        logging.debug(f"   Truncated text = {text}")

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = crf_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.crf_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    result_list, lang_code = wrapper_util.get_nlpe_engine().retrieve_crf_entities(name,
                                                                                  text, lang_code,
                                                                                  meta_info.weak_match_threshold)

    # return status, [{"entity": "location", "index": 31, "len": 8}, ...]
    return 200, result_list
