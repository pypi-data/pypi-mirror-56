"""
Wrapper of Feersum_NLU's Dashboard Python API in HTTP API.
"""

from typing import Tuple, Dict, List, Optional  # noqa # pylint: disable=unused-import
# import json

from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import __version__ as feersum_nlu_sdk_version


@wrapper_util.lock_decorator_nlpe
@wrapper_util.auth_decorator
def dashboard_get_details(auth_token: str,
                          caller_name: Optional[str],
                          show_data_objects: Optional[bool],
                          history_size: Optional[int]) -> Tuple[int, wrapper_util.JSONType]:
    # object = {name: str, id: str, model_type: str, collection_uri: str, api_hit_count: integer}
    model_list = []  # type: List[Dict]

    # === Generic date_parser ===
    model_list.append({'name': 'generic',
                       'long_name': 'Generic date_parser.',
                       'desc': 'Generic pre-created date parser.',
                       'model_type': 'date_parser',
                       'collection_uri': '/date_parsers',
                       "trashed": False})

    # === Generic sentiment_detector ===
    model_list.append({'name': 'generic',
                       'long_name': 'Generic sentiment_detector.',
                       'desc': 'Generic pre-created sentiment detector.',
                       'model_type': 'sentiment_detector',
                       'collection_uri': '/sentiment_detectors',
                       "trashed": False})

    # === Built-in language models - typically lazy loaded on first use. ===
    for name in wrapper_util.nlp_engine.feers_sent_encoder_dict:
        model_list.append({'name': name, 'desc': wrapper_util.nlp_engine.feers_sent_encoder_long_name_dict.get(name),
                           'long_name': wrapper_util.nlp_engine.feers_sent_encoder_long_name_dict.get(name),
                           'model_type': 'sentence_encoder',
                           'collection_uri': '/sentence_encoders',
                           'sentence_encoder_type': wrapper_util.nlp_engine.feers_sent_encoder_type_dict.get(name),
                           "trashed": False})

    # === Models listed in DB ===
    model_info_list = wrapper_util.load_model_list(
        auth_token=auth_token,
        show_data_objects=show_data_objects)  # List[Tuple[name, uuid, trashed, desc, long_name]]

    for model_info in model_info_list:
        name = model_info[0]
        uuid = model_info[1]
        trashed = model_info[2]
        desc = model_info[3]
        long_name = model_info[4]

        if auth_token in name:
            model_type = None  # type: Optional[str]
            collection_uri = None

            if name.endswith('.duckling_extr_meta_pickle'):
                model_type = 'duckling_entity_extractor'
                collection_uri = '/duckling_entity_extractors'
            elif name.endswith('.faq_matcher_meta_pickle'):
                model_type = 'faq_matcher'
                collection_uri = '/faq_matchers'
            elif name.endswith('.intent_clsfr_meta_pickle'):
                model_type = 'intent_classifier'
                collection_uri = '/intent_classifiers'
            elif name.endswith('.lr4_language_recogniser_meta_pickle'):
                model_type = 'language_recogniser'
                collection_uri = '/language_recognisers'
            elif name.endswith('.person_name_extr_meta_pickle'):
                model_type = 'person_name_entity_extractor'
                collection_uri = '/person_name_entity_extractors'
            elif name.endswith('.crf_extr_meta_pickle'):
                model_type = 'crf_entity_extractor'
                collection_uri = '/crf_entity_extractors'
            elif name.endswith('.regex_extr_meta_pickle'):
                model_type = 'regex_entity_extractor'
                collection_uri = '/regex_entity_extractors'
            elif name.endswith('.sim_word_extr_meta_pickle'):
                model_type = 'sim_word_entity_extractor'
                collection_uri = '/sim_word_entity_extractors'
            elif name.endswith('.synonym_extr_meta_pickle'):
                model_type = 'synonym_entity_extractor'
                collection_uri = '/synonym_entity_extractors'
            elif name.endswith('.text_clsfr_meta_pickle'):
                model_type = 'text_classifier'
                collection_uri = '/text_classifiers'
            elif name.endswith('.data_object_meta_pickle'):
                model_type = 'data_object'
                collection_uri = '/data_objects'
            elif name.endswith('.image_clsfr_meta_pickle'):
                model_type = 'image_classifier'
                collection_uri = '/image_classifiers'
            elif name.endswith('.language_model_pickle'):
                model_type = 'sentence_encoder'
                collection_uri = '/sentence_encoders'
            elif name.endswith('.vision_model_pickle'):
                model_type = 'image_encoder'
                collection_uri = '/image_encoders'

            name_sans_auth_token = name.replace('_' + auth_token, '')
            index_of_last_dot = name_sans_auth_token.rfind('.')
            name_sans_auth_token_sans_ext = name_sans_auth_token[:index_of_last_dot]

            if history_size is None:
                history_size = 5

            # json List[{version, uuid, message}]
            model_history = wrapper_util.load_model_history(name=name, history_size=history_size)

            model_list.append({'name': name_sans_auth_token_sans_ext,
                               'uuid': uuid,
                               'long_name': long_name,
                               'desc': desc,
                               'model_type': model_type,
                               'collection_uri': collection_uri,
                               'trashed': trashed,
                               'history': model_history})

    model_list.sort(key=lambda model: model.get('name'))

    # === Dashboard and API level things ===

    dash_content = {
        'api_version': feersum_nlu_sdk_version,
        'model_list': model_list,
        'service_name': 'FeersumNLU Service',
        'log_file': wrapper_util.get_log_filename()
    }

    return 200, dash_content
