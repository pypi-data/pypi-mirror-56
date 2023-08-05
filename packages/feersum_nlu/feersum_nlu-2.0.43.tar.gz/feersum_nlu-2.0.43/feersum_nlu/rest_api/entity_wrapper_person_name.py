"""
Wrapper of Feersum_NLU's Person Name Entity Extractor Python API in HTTP API.
"""
from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
import uuid
import logging

from feersum_nlu.rest_api import wrapper_util


def person_name_extr_save_helper(name: str, model_save_mode: wrapper_util.SaveHelperMode,
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
        # wrapper_util.get_wrapper_nlpe_engine().vaporise_person_name_extr(name)
        pass
    elif model_save_mode == wrapper_util.SaveHelperMode.SAVE_MODEL:
        # Save the model blob.
        # success = wrapper_util.get_wrapper_nlpe_engine().save_person_name_extr(name)
        #
        # if not success:
        #     return False
        pass
    else:
        # Don't save and don't vaporise.
        pass

    # Then save the meta info with updated uuid ...
    meta_info = wrapper_util.person_name_extr_dict[name]  # At this point one can assume that the key exists.

    meta_info.uuid = str(uuid.uuid4())  # Update the uuid of the local copy.

    success = wrapper_util.save_meta_info_blob(name + '.person_name_extr_meta_pickle', meta_info,
                                               save_in_history=save_in_history,
                                               save_in_history_message=save_in_history_message)

    if not success:
        return False

    return True


def person_name_extr_upgrade_meta_info(meta_info):
    # Check for older versions of meta_info
    upgrade_meta_info = False

    if hasattr(meta_info, 'readonly') is False:
        upgrade_meta_info = True
        meta_info_readonly = False
    else:
        meta_info_readonly = meta_info.readonly

    if upgrade_meta_info:
        logging.debug(f"    entity_wrapper_person_name.person_name_extr_load_helper: Upgrading meta_info.")
        meta_info = wrapper_util.PersonNameExtractorMeta(meta_info.uuid,
                                                         meta_info.long_name,
                                                         meta_info.desc,
                                                         meta_info_readonly)
    return meta_info


def person_name_extr_load_history_helper(name: str,
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
        logging.error(f"person_name_extr_load_history_helper: Model history meta_info for {name} is not available!")
        person_name_extr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.PersonNameExtractorMeta):
        logging.error(f"person_name_extr_load_history_helper: Loaded model meta_info of {name} of incorrect class!")
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.person_name_extr_dict.get(name) is not meta_info:
        meta_info = person_name_extr_upgrade_meta_info(meta_info)
        wrapper_util.person_name_extr_dict[name] = meta_info

        # Note: If a revision was retrieved from history then the model needs to be RETRAINED! So trash the cached model.
        # wrapper_util.get_nlpe_engine().trash_person_name_extr(name, trash_cache_only=True)

        success = wrapper_util.save_meta_info_blob(name + '.person_name_extr_meta_pickle', meta_info,
                                                   save_in_history=True,
                                                   save_in_history_message=f"Restored {meta_info.uuid}.")
        return success

    return True


def person_name_extr_load_helper(name: str,
                                 look_in_trash: bool) -> bool:
    """
    Load the meta info and model info + manage local cache.

    :param name: The name_apikey of the model e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a
    :param look_in_trash: Will load the model even if the trashed flag in the meta info is True.
    :return: True if success; False otherwise.
    """

    meta_info = wrapper_util.load_meta_info_blob(name=name + '.person_name_extr_meta_pickle',
                                                 look_in_trash=look_in_trash,
                                                 cached_meta_blob=wrapper_util.person_name_extr_dict.get(name))

    if meta_info is None:
        # Model not available so delete local meta info and model cache and return failure.
        person_name_extr_trash_helper(name, trash_cache_only=True)
        return False  # 400, {"error_detail": "Loading of model meta data failed!"}

    if not isinstance(meta_info, wrapper_util.PersonNameExtractorMeta):
        return False  # 400, {"error_detail": "Loaded model meta_info object of incorrect class!"}

    # Then try and load the model ...
    # If local cached meta_info different from loaded meta_info OR if meta_info not cached yet
    # then update cache and load the NLPE model.
    if wrapper_util.person_name_extr_dict.get(name) is not meta_info:
        meta_info = person_name_extr_upgrade_meta_info(meta_info)
        wrapper_util.person_name_extr_dict[name] = meta_info

        # Try to load the model.
        # wrapper_util.get_wrapper_nlpe_engine().load_person_name_extr(name)

    return True


def person_name_extr_trash_helper(name: str, trash_cache_only: bool = False) -> bool:
    """ Trash the meta info and model info + manage cache. """

    if wrapper_util.person_name_extr_dict.get(name) is not None:
        del wrapper_util.person_name_extr_dict[name]

    if not trash_cache_only:
        wrapper_util.trash_meta_info_blob(name + '.person_name_extr_meta_pickle')

    # wrapper_util.get_wrapper_nlpe_engine().trash_person_name_extr(name, trash_cache_only=trash_cache_only)

    return True


def person_name_extr_vaporise_helper(name: str) -> bool:
    """ Vaporise the meta info and model info + manage cache. """

    if wrapper_util.person_name_extr_dict.get(name) is not None:
        del wrapper_util.person_name_extr_dict[name]

    wrapper_util.vaporise_meta_info_blob(name + '.person_name_extr_meta_pickle')

    # wrapper_util.get_wrapper_nlpe_engine().vaporise_person_name_extr(name)

    return True


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_create(iname: str,
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
            success = person_name_extr_load_history_helper(name, revision_uuid)
        else:
            success = person_name_extr_load_helper(name, look_in_trash=True)

        meta_info = wrapper_util.person_name_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Loading from store failed!"}

        return 200, {"name": iname,
                     "id": meta_info.uuid,
                     "long_name": meta_info.long_name,
                     "desc": meta_info.desc,
                     "readonly": meta_info.readonly}
    else:
        # === See if there already exists a model with the same name ===
        success = person_name_extr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.person_name_extr_dict.get(name)

        if success and meta_info is not None:
            # The model already exists; check if it is readonly before creating a new one with the same name.
            if meta_info.readonly:
                return 400, {"error_detail": "Named instance {} exists and is readonly!".format(iname)}  # Bad request.
        # === ===

        # Create a new model
        # not implemented in the nlpe layer yet.

        # Create the meta_info
        wrapper_util.person_name_extr_dict[name] = wrapper_util.PersonNameExtractorMeta("",
                                                                                        long_name,
                                                                                        description,
                                                                                        False)

        # Save the named meta_info and model blobs. MIGHT modify the meta_info!
        success = person_name_extr_save_helper(name, wrapper_util.SaveHelperMode.SAVE_MODEL,
                                               save_in_history=True,
                                               save_in_history_message="Created model.")

        return 200, {"name": iname,
                     "id": wrapper_util.person_name_extr_dict[name].uuid,
                     "long_name": wrapper_util.person_name_extr_dict[name].long_name,
                     "desc": wrapper_util.person_name_extr_dict[name].desc,
                     "readonly": wrapper_util.person_name_extr_dict[name].readonly}


#########################
#########################
#########################
#########################


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_del(iname: str, auth_token: str, caller_name: Optional[str],
                         vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the person_name extractor model. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    person_name_extr_details = {}  # type: Dict

    # Load the meta_info blob and the nlpe model blob into memory ONLY to return the details.
    if not vaporise:
        success = person_name_extr_load_helper(name, look_in_trash=False)
        meta_info = wrapper_util.person_name_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}
    else:
        success = person_name_extr_load_helper(name, look_in_trash=True)
        meta_info = wrapper_util.person_name_extr_dict.get(name)

        if not success or meta_info is None:
            return 400, {"error_detail": "Named instance {} not loaded and not in trash!".format(iname)}

    # Details of model stored in wrapper.
    person_name_extr_details = {"name": name[:-(len(auth_token) + 1)],
                                "id": meta_info.uuid,
                                "long_name": meta_info.long_name,
                                "desc": meta_info.desc,
                                "readonly": meta_info.readonly}

    if not vaporise:
        person_name_extr_trash_helper(name)
    else:
        person_name_extr_vaporise_helper(name)

    return 200, person_name_extr_details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_get_details(iname: str, auth_token: str,
                                 caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = person_name_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.person_name_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    # Details of classifier stored in wrapper.
    person_name_extr_details = {"name": iname,
                                "id": meta_info.uuid,
                                "long_name": meta_info.long_name,
                                "desc": meta_info.desc,
                                "readonly": meta_info.readonly}

    return 200, person_name_extr_details


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_get_details_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    details_list = []  # type: List[Dict]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.faq_matcher_meta_pickle'

        if name.endswith('.person_name_extr_meta_pickle'):
            meta_info = model_info[1]  # type: wrapper_util.PersonNameExtractorMeta

            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

            # Details of classifier stored in wrapper.
            details_list.append({"name": name_sans_auth_token_sans_ext,
                                 "id": meta_info.uuid,
                                 "long_name": meta_info.long_name,
                                 "desc": meta_info.desc,
                                 "readonly": meta_info.readonly
                                 if hasattr(meta_info, 'readonly') else False})

    return 200, details_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_retrieve(iname: str, auth_token: str, caller_name: Optional[str],
                              text: Optional[str], lang_code: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
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
    success = person_name_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.person_name_extr_dict.get(name)

    # Test server latency.
    # time.sleep(1.0)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.

    # List[Dict / primitive]
    result_list = wrapper_util.get_nlpe_engine().retrieve_person_name_entities(text)

    return 200, result_list


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_set_params(iname: str, auth_token: str, caller_name: Optional[str],
                                param_dict: Dict) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    new_iname = param_dict.get('name')
    long_name = param_dict.get('long_name')
    desc = param_dict.get('desc')
    readonly = param_dict.get('readonly')

    # Load the meta_info blob and the nlpe model blob into memory.
    success = person_name_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.person_name_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    if meta_info.readonly and (readonly is None or readonly is True):
        return 400, {"error_detail": "Named instance {} is readonly!".format(iname)}  # Bad/Malformed request.

    meta_info = wrapper_util.PersonNameExtractorMeta(meta_info.uuid,
                                                     meta_info.long_name,
                                                     meta_info.desc,
                                                     meta_info.readonly)

    if new_iname is not None and new_iname != iname:
        # new_name = new_iname + "_" + auth_token
        # print("    Change of name not implemented yet!")
        pass

    if long_name is not None:
        meta_info.long_name = long_name
    if desc is not None:
        meta_info.desc = desc
    if readonly is not None:
        meta_info.readonly = readonly

    wrapper_util.person_name_extr_dict[name] = meta_info

    # Save the named meta_info blob. MIGHT modify the meta_info!
    success = person_name_extr_save_helper(name, wrapper_util.SaveHelperMode.DONT_SAVE_MODEL,
                                           save_in_history=True,
                                           save_in_history_message="Updated parameters.")

    if not success:
        return 500, {"error_detail": "Saving of model meta data failed!"}

    return 200, {"name": iname,
                 "id": wrapper_util.person_name_extr_dict[name].uuid,
                 "long_name": wrapper_util.person_name_extr_dict[name].long_name,
                 "desc": wrapper_util.person_name_extr_dict[name].desc,
                 "readonly": wrapper_util.person_name_extr_dict[name].readonly}


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def person_name_extr_get_params(iname: str, auth_token: str,
                                caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Load the meta_info blob and the nlpe model blob into memory.
    success = person_name_extr_load_helper(name, look_in_trash=False)
    meta_info = wrapper_util.person_name_extr_dict.get(name)

    if not success or meta_info is None:
        return 400, {"error_detail": "Named instance {} not loaded!".format(iname)}  # Bad/Malformed request.s

    return 200, {"long_name": meta_info.long_name,
                 "desc": meta_info.desc,
                 "readonly": meta_info.readonly}
