"""
Wrapper of Feersum_NLU's Data Object Python API in HTTP API.
"""
from typing import Tuple, List, Optional  # noqa # pylint: disable=unused-import
import uuid

from feersum_nlu.rest_api import wrapper_util


#########################
#########################
@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_post(iname: str,
                     auth_token: str, caller_name: Optional[str],
                     object_data: wrapper_util.JSONType) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None or iname == "":
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    # Always update the DB - i.e. no local cache kept of data objects!
    meta_info = wrapper_util.DataObjectMeta(str(uuid.uuid4()), object_data)

    success = wrapper_util.save_meta_info_blob(name + '.data_object_meta_pickle', meta_info,
                                               save_in_history=True,
                                               save_in_history_message="data_object_post")

    if not success or meta_info is None:
        return 400, {"error_detail": "data_object_post failed!"}

    return 200, object_data


#########################
#########################
@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_del(iname: str, auth_token: str, caller_name: Optional[str],
                    vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise the data object. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    meta_info = wrapper_util.load_meta_info_blob(name=name + '.data_object_meta_pickle',
                                                 look_in_trash=vaporise,
                                                 cached_meta_blob=None)

    if meta_info is None:
        return 400, {"error_detail": f"Named instance {iname} not found!"}  # Bad/Malformed request.

    if vaporise:
        wrapper_util.vaporise_meta_info_blob(name + '.data_object_meta_pickle')
    else:
        wrapper_util.trash_meta_info_blob(name + '.data_object_meta_pickle')

    return 200, meta_info.data


@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_undelete(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    """ Bring the data object back from the trash. """
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token

    meta_info = wrapper_util.load_meta_info_blob(name=name + '.data_object_meta_pickle',
                                                 look_in_trash=True,
                                                 cached_meta_blob=None)

    # Note: The object is automatically untrashed if loaded from the trash!

    if meta_info is None:
        return 400, {"error_detail": f"Named instance {iname} not found in trash!"}  # Bad/Malformed request.

    return 200, meta_info.data


@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_del_all(auth_token: str, caller_name: Optional[str],
                        vaporise: bool) -> Tuple[int, wrapper_util.JSONType]:
    """ Trash/vaporise all the data objects for this auth_token. """
    # === Models listed in DB ===
    names_list = []  # type: List[str]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.type_meta_pickle'

        if auth_token in name:
            if name.endswith('.data_object_meta_pickle'):
                name_sans_auth_token = name.replace('_' + auth_token, '')
                index_of_last_dot = name_sans_auth_token.rfind('.')
                name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

                if vaporise:
                    wrapper_util.vaporise_meta_info_blob(name)
                else:
                    wrapper_util.trash_meta_info_blob(name)

                names_list.append(name_sans_auth_token_sans_ext)

    return 200, names_list


@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_get_details(iname: str, auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    if iname is None:
        return 400, {"error_detail": "No instance name provided!"}  # Bad/Malformed request.

    name = iname + "_" + auth_token
    meta_info = wrapper_util.load_meta_info_blob(name=name + '.data_object_meta_pickle',
                                                 look_in_trash=False,
                                                 cached_meta_blob=None)
    # ToDo: Consider using a cache dict in `cached_meta_blob` like for other models if performance becomes a problem.

    if meta_info is None:
        return 400, {"error_detail": f"Named instance {iname} not found!"}  # Bad/Malformed request.

    return 200, meta_info.data


@wrapper_util.lock_decorator_data
@wrapper_util.auth_decorator
def data_object_get_names_all(auth_token: str, caller_name: Optional[str]) -> Tuple[int, wrapper_util.JSONType]:
    names_list = []  # type: List[str]

    model_meta_info_list = \
        wrapper_util.load_model_meta_info_list(auth_token=auth_token)  # List[Tuple[name, meta_info object]]

    for model_info in model_meta_info_list:
        name = model_info[0]  # name is 'modelname_authtoken.type_meta_pickle'

        if name.endswith('.data_object_meta_pickle'):
            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

            names_list.append(name_sans_auth_token_sans_ext)

    return 200, names_list
