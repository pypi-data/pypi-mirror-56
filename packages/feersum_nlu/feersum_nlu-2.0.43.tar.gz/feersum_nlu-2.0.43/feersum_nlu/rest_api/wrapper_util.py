# import psutil
import io
import time
import threading
from typing import List, Set, Dict, Tuple, Any, Optional, Union, Iterable
from enum import Enum
# from inspect import getfullargspec
import pickle
# from datetime import datetime
import logging

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data

from feersum_nlu import vision_engine

from feersum_nlu.db_models import WrapperBlobData
from feersum_nlu.db_models import WrapperBlobDataVersioned
from feersum_nlu.db_models import APIKeyData
from feersum_nlu.db_models import AdminAPIKeyData
from feersum_nlu.db_models import APICallCountBreakdownData

from feersum_nlu.rest_flask_utils import db
from feersum_nlu.rest_flask_utils import get_log_filename
from feersum_nlu import __pickle_protocol_version__ as feersum_nlu_pickle_protocol_version

from sqlalchemy.orm import load_only

from prometheus_client import Gauge

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

# ToDo: Consider splitting this file into db_util.py and wrapper_util.py so that the db management can happen without having
#       to import wrapper things.

#
#  Module global variable that store if the default auth tokens have been lazily configured.
__default_auth_tokens_configured = False

# Lock for access to the single NLPEngine instance defined in wrapper_util. Note: The lock is meant to protect against
# multi-threaded access and doesn't impact pre-forked multi-process execution!

# ToDo: Use multiple sessions for the different threads accessing the DB. A session is not thread safe!!!
# - https://docs.sqlalchemy.org/en/13/orm/contextual.html#unitofwork-contextual
# Once multiple sessions are used the different locks for nlpe, vise, data & health can be used.
# NOTE!!! - auth_decorator is also not thread safe yet!
__nlpe_wrapper_lock = threading.Lock()
__vise_wrapper_lock = __nlpe_wrapper_lock  # threading.Lock() - See note above.
__data_wrapper_lock = __nlpe_wrapper_lock  # threading.Lock() - See note above.
__health_wrapper_lock = __nlpe_wrapper_lock  # threading.Lock() - See note above.

intent_retrieve_MAX_TEXT_LENGTH = -1  # type: int
faq_retrieve_MAX_TEXT_LENGTH = -1  # type: int
entity_retrieve_MAX_TEXT_LENGTH = -1  # type: int

# === Create the NLPEngine ===
__nlpe = None  # Optional[nlp_engine.NLPEngine]


def start_nlp_engine(use_duckling: bool = True):
    """ Start the wrapper's NLPEngine with or without Duckling. """
    global __nlpe

    logging.info(f"start_nlp_engine: Log file is {get_log_filename()}.")
    logging.info(f"start_nlp_engine: Starting NLP Engine.")
    __nlpe = nlp_engine.NLPEngine(use_duckling=use_duckling)

    return __nlpe


def get_nlpe_engine(use_duckling: bool = True) -> nlp_engine.NLPEngine:
    """ Get (and perhaps lazily start with or without Duckling) the wrapper's NLPEngine. """
    global __nlpe

    if __nlpe is None:
        logging.info(f"start_nlp_engine: Starting NLP Engine.")
        __nlpe = nlp_engine.NLPEngine(use_duckling=use_duckling)

    return __nlpe


# =============================


# === Create the VisionEngine ===
__vise = None  # Optional[vision_engine.VisionEngine]


def start_vision_engine():
    """ Start the wrapper's VisionEngine. """
    global __vise

    logging.info(f"start_vision_engine: Log file is {get_log_filename()}.")
    logging.info(f"start_vision_engine: Starting Vision Engine.")
    __vise = vision_engine.VisionEngine()

    return __vise


def get_vision_engine() -> vision_engine.VisionEngine:
    """ Get (and perhaps lazily start) the wrapper's VisionEngine. """
    global __vise

    if __vise is None:
        logging.info(f"start_vision_engine: Starting Vision Engine.")
        __vise = vision_engine.VisionEngine()

    return __vise


# =============================


# === The meta info classes for all of the model types ===
class PersonNameExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly


class DucklingExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _reference_time: Optional[str]) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.reference_time = _reference_time


class RegExpExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _regex: str,
                 _training_stamp: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.regex = _regex
        self.training_stamp = _training_stamp


class SimWordExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _input_entities: Set[str],
                 _threshold: float,
                 _word_manifold_name: str,
                 _spell_correct: bool,
                 _training_stamp: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.input_entities = _input_entities
        self.threshold = _threshold
        self.word_manifold_name = _word_manifold_name
        self.spell_correct = _spell_correct
        self.training_stamp = _training_stamp


class FAQMatcherMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _testing_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _validation_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _testing_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _confusion_dict_labels: Dict[str, str],
                 _training_stamp: str,
                 _tsne_results: Optional[Dict],
                 _word_manifold_name_dict: Dict[str, str]) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold

        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_confusion_dict = _training_confusion_dict
        self.validation_confusion_dict = _training_confusion_dict
        self.testing_confusion_dict = _testing_confusion_dict

        self.confusion_dict_labels = _confusion_dict_labels

        self.training_stamp = _training_stamp
        self.tsne_results = _tsne_results

        self.word_manifold_name_dict = _word_manifold_name_dict


class IntentClassifierMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _testing_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _validation_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _testing_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _confusion_dict_labels: Dict[str, str],
                 _training_stamp: str,
                 _tsne_results: Optional[Dict],
                 _word_manifold_name_dict: Dict[str, str]) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold

        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_confusion_dict = _training_confusion_dict
        self.validation_confusion_dict = _training_confusion_dict
        self.testing_confusion_dict = _testing_confusion_dict

        self.confusion_dict_labels = _confusion_dict_labels

        self.training_stamp = _training_stamp
        self.tsne_results = _tsne_results

        self.word_manifold_name_dict = _word_manifold_name_dict


class LR4LanguageRecogniserMeta(object):
    def __init__(self, _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _txt_clsfr_model_name: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.txt_clsfr_model_name = _txt_clsfr_model_name


class ImageClassifierMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Tuple[str, str, str]],  # image, label, uuid
                 _testing_samples: List[Tuple[str, str, str]],  # image, label, uuid
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _validation_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _testing_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _confusion_dict_labels: Dict[str, str],
                 _training_stamp: str,
                 _clsfr_algorithm: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold

        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_confusion_dict = _training_confusion_dict
        self.validation_confusion_dict = _validation_confusion_dict
        self.testing_confusion_dict = _testing_confusion_dict

        self.confusion_dict_labels = _confusion_dict_labels

        self.training_stamp = _training_stamp

        self.clsfr_algorithm = _clsfr_algorithm


class NTCMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _testing_samples: List[Tuple[str, str, str, str]],  # text, label, text language hint, uuid.
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _validation_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _testing_confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                 _confusion_dict_labels: Dict[str, str],
                 _training_stamp: str,
                 _tsne_results: Optional[Dict],
                 _clsfr_algorithm: str,
                 _language_model_name_dict: Dict[str, str]) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold

        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_confusion_dict = _training_confusion_dict
        self.validation_confusion_dict = _validation_confusion_dict
        self.testing_confusion_dict = _testing_confusion_dict

        self.confusion_dict_labels = _confusion_dict_labels

        self.training_stamp = _training_stamp
        self.tsne_results = _tsne_results

        self.clsfr_algorithm = _clsfr_algorithm
        self.language_model_name_dict = _language_model_name_dict


class CRFExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Dict],
                 _testing_samples: List[Dict],
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_stamp: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold
        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_stamp = _training_stamp


class SynonymExtractorMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _weak_match_threshold: float,
                 _training_samples: List[Dict],
                 _testing_samples: List[Dict],
                 _training_accuracy: float,
                 _validation_accuracy: float,
                 _testing_accuracy: float,
                 _training_f1: float,
                 _validation_f1: float,
                 _testing_f1: float,
                 _training_stamp: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.weak_match_threshold = _weak_match_threshold
        self.training_samples = _training_samples
        self.testing_samples = _testing_samples

        self.training_accuracy = _training_accuracy
        self.validation_accuracy = _training_accuracy
        self.testing_accuracy = _testing_accuracy

        self.training_f1 = _training_f1
        self.validation_f1 = _training_f1
        self.testing_f1 = _testing_f1

        self.training_stamp = _training_stamp


class WordManifoldMeta(object):
    def __init__(self,
                 _uuid: str,
                 _long_name: Optional[str],
                 _desc: Optional[str],
                 _readonly: bool,
                 _vectors_file: str) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.long_name = _long_name
        self.desc = _desc
        self.readonly = _readonly
        self.vectors_file = _vectors_file


class DataObjectMeta(object):
    def __init__(self,
                 _uuid: str,
                 _data: JSONType) -> None:
        self.uuid = _uuid  # Unique version identifier.
        self.data = _data


# === ===


# === The model instance dictionaries; Local cache for the models; Maintained by the various wrapper modules ===
wm_dict = {}  # type: Dict[str, WordManifoldMeta]
ntc_dict = {}  # type: Dict[str, NTCMeta]
person_name_extr_dict = {}  # type: Dict[str, PersonNameExtractorMeta]
duckling_extr_dict = {}  # type: Dict[str, DucklingExtractorMeta]
crf_extr_dict = {}  # type: Dict[str, CRFExtractorMeta]
synonym_extr_dict = {}  # type: Dict[str, SynonymExtractorMeta]
regex_extr_dict = {}  # type: Dict[str, RegExpExtractorMeta]
sim_word_extr_dict = {}  # type: Dict[str, SimWordExtractorMeta]
faq_dict = {}  # type: Dict[str, FAQMatcherMeta]
intent_clsfr_dict = {}  # type: Dict[str, IntentClassifierMeta]
lr4_language_recogniser_dict = {}  # type: Dict[str, LR4LanguageRecogniserMeta]

image_classifier_dict = {}  # type: Dict[str, ImageClassifierMeta]

# Cache of API call count and call count limit tuples (call_count, call_count_limit)
auth_token_call_cache = {}  # type: Dict[str, Tuple[int,Optional[int]]]
auth_token_desc_cache = {}  # type: Dict[str, str]

# === ===
# RED:
# Rate - the number of requests, per second, you services are serving.
# Errors - the number of failed requests per second.
# Duration - distributions of the amount of time each request takes.

# promths_request_histogrm = Histogram('feersum_nlu_request_latency_seconds', 'FeersumNLU - Request Latency',
#                                      ['endpoint'])

promths_idle_fraction_gauge = Gauge('feersum_nlu_wrapper_idle_fraction', 'FeersumNLU - Wrapper Idle Fraction')
last_operation_start_time = 0.0
last_operation_end_time = 0.0

# This server's request latency.
promths_request_latency_gauge = Gauge('feersum_nlu_request_latency_seconds', 'FeersumNLU - Request Latency',
                                      ['endpoint'])

# This server's number of unauthorised denied calls.
promths_call_count_gauge_unauthrsd = Gauge('feersum_nlu_unauthrsd_call_count',
                                           'FeersumNLU - Number of unauthorised & denied calls.',
                                           ['auth_desc'])

# The call count across all servers (cached locally, but updated regularly from the DB). May be used for billing!
promths_call_count_gauge_authrsd = Gauge('feersum_nlu_api_call_count', 'FeersumNLU - API Call Count',
                                         ['auth_desc'])

# This server's http responses
promths_http_response_gauge = Gauge('feersum_nlu_http_responses',
                                    'FeersumNLU - HTTP Responses.',
                                    ['auth_desc', 'endpoint', 'status'])


# promths_call_units_histogrm = Histogram('feersum_nlu_api_call_units', 'FeersumNLU - API Call Units',
#                                         ['endpoint'])


def lock_decorator_nlpe(f):
    """
    Decorator to protect access to the wrapper_util nlpe instance below and its wrapper functions
    using nlpe_wrapper_lock. NOTE: This lock is meant to queue multi-threaded access to the service wrapper.
    """

    def decorated_f(*args, **kwargs):
        # pre_lock_time = time.time()

        __nlpe_wrapper_lock.acquire()

        # start_time = time.time()
        # logging.info(f"lock_decorator_nlpe: __nlpe_wrapper_lock acquired in {start_time - pre_lock_time}s")

        try:
            response_code, response_json = f(*args, **kwargs)
        except Exception as e:
            logging.exception(f"lock_decorator_nlpe: Uncaught exception: {e}!")
            promths_http_response_gauge.labels(auth_desc=f"[Uncaught exception: {str(e)}]",  # pylint: disable=no-member
                                               endpoint=f.__name__, status=500).inc()  # pylint: disable=no-member
            raise  # re-raise the uncaught exception.
        finally:  # call release when try block is finished or before uncaught exceptions raised.
            __nlpe_wrapper_lock.release()

            # end_time = time.time()
            # logging.info(f"lock_decorator_nlpe: __nlpe_wrapper_lock duration = {round(end_time - start_time, 4)}s  "
            #              f"end_time = {datetime.now()}")

        return response_code, response_json

    return decorated_f


def lock_decorator_vise(f):
    """
    Decorator to protect access to the wrapper_util vise instance below and its wrapper functions
    using vise_wrapper_lock. NOTE: This lock is meant to queue multi-threaded access to the service wrapper.
    """

    def decorated_f(*args, **kwargs):
        # pre_lock_time = time.time()

        __vise_wrapper_lock.acquire()

        # start_time = time.time()
        # logging.info(f"lock_decorator_vise: __vise_wrapper_lock acquired in {start_time - pre_lock_time}s")

        try:
            response_code, response_json = f(*args, **kwargs)
        except Exception as e:
            logging.exception(f"lock_decorator_vise: Uncaught exception: {e}!")
            raise  # re-raise the uncaught exception.
        finally:  # call release when try block is finished or before uncaught exceptions raised.
            __vise_wrapper_lock.release()

            # end_time = time.time()
            # logging.info(f"lock_decorator_vise: __vise_wrapper_lock duration = {round(end_time - start_time, 4)}s  "
            #              f"end_time = {datetime.now()}")

        return response_code, response_json

    return decorated_f


def lock_decorator_data(f):
    """
    Decorator to protect access to the data endpoints and its wrapper functions
    using data_wrapper_lock. NOTE: This lock is meant to queue multi-threaded access to the service wrapper.
    """

    def decorated_f(*args, **kwargs):
        # pre_lock_time = time.time()

        __data_wrapper_lock.acquire()

        # start_time = time.time()
        # logging.info(f"lock_decorator_data: __data_wrapper_lock acquired in {start_time - pre_lock_time}s")

        try:
            response_code, response_json = f(*args, **kwargs)
        except Exception as e:
            logging.exception(f"lock_decorator_data: Uncaught exception: {e}!")
            raise  # re-raise the uncaught exception.
        finally:  # call release when try block is finished or before uncaught exceptions raised.
            __data_wrapper_lock.release()

            # end_time = time.time()
            # logging.info(f"lock_decorator_data: __data_wrapper_lock duration = {round(end_time - start_time, 4)}s  "
            #              f"end_time = {datetime.now()}")

        return response_code, response_json

    return decorated_f


def lock_decorator_health(f):
    """
    Decorator to protect access to the health endpoints and its wrapper functions
    using health_wrapper_lock. NOTE: This lock is meant to queue multi-threaded access to the service wrapper.
    """

    def decorated_f(*args, **kwargs):
        # pre_lock_time = time.time()

        __health_wrapper_lock.acquire()

        # start_time = time.time()
        # logging.info(f"lock_decorator_health: __health_wrapper_lock acquired in {start_time - pre_lock_time}s")

        try:
            response_code, response_json = f(*args, **kwargs)
        except Exception as e:
            logging.exception(f"lock_decorator_health: Uncaught exception: {e}!")
            raise  # re-raise the uncaught exception.
        finally:  # call release when try block is finished or before uncaught exceptions raised.
            __health_wrapper_lock.release()

            # end_time = time.time()
            # logging.info(f"lock_decorator_health: __health_wrapper_lock duration = {round(end_time - start_time, 4)}s  "
            #              f"end_time = {datetime.now()}")

        return response_code, response_json

    return decorated_f


def auth_decorator(f):
    """
    Decorator to check that an auth token was provided and that it is valid and
    to log info on the wrapper layer functions.
    """

    def decorated_f(*args, **kwargs):
        global last_operation_start_time
        global last_operation_end_time

        current_time = time.time()

        if last_operation_end_time != 0.0:
            idle_time = round(current_time - last_operation_end_time, 4)
            total_time = round(current_time - last_operation_start_time, 4)
            promths_idle_fraction_gauge.set(idle_time / total_time)

        last_operation_start_time = current_time

        # === Find auth_token amongst the named parameters ===
        auth_token = kwargs.get('auth_token')
        # ====================================================
        caller_name = kwargs.get('caller_name')

        # if 'image' in f.__name__:
        #     logging.info(f"rest_wrapper_request: {f.__name__ } <- [arguments not shown] (caller_name={caller_name})")
        # else:
        #     logging.info(f"rest_wrapper_request: {f.__name__} <- {str(args)} {str(kwargs)}")

        # === Check that an auth token was provided ===
        if auth_token is None:
            promths_call_count_gauge_unauthrsd.labels(auth_desc="None").inc()  # pylint: disable=no-member
            logging.info(f"auth_decorator: None: No authorisation token provided!")
            last_operation_end_time = time.time()
            return 403, {"error_detail": "No authorisation token provided!"}  # Bad/Malformed request.
        # =============================================

        auth_desc = auth_token_desc_cache.get(auth_token, "[Not in cache!]")

        # === Check that the auth token is valid ===
        if not is_auth_token_valid(auth_token):  # Note: Also updates the local call count cache!
            logging.info(f"auth_decorator: {auth_token}: Invalid authorisation token or API rate limit exceeded!")
            promths_call_count_gauge_unauthrsd.labels(auth_desc=auth_desc).inc()  # pylint: disable=no-member
            last_operation_end_time = time.time()
            return 403, {"error_detail": "Invalid authorisation token provided or API rate limit exceeded!"}
        # ==========================================

        # === Update desc. to latest cached value after update in is_auth_token_valid ^ ===
        auth_desc = auth_token_desc_cache.get(auth_token, "[Not in cache!]")
        # =================================================================================

        start_time = time.time()

        # === Call the wrapper layer function ===
        response_code, response_json = f(*args, **kwargs)
        # =======================================

        call_duration = round(time.time() - start_time, 4)

        # logging.info(f"rest_wrapper_response: {f.__name__} -> {str((response_code, response_json))} "
        #              f"in {call_duration} seconds.")

        promths_http_response_gauge.labels(auth_desc=auth_desc,  # pylint: disable=no-member
                                           endpoint=f.__name__, status=response_code).inc()  # pylint: disable=no-member

        if 200 <= response_code <= 299:
            # The API call was successful - Update call count & log/monitor.

            text = kwargs.get('text')

            # === Count one call unit per 100 chars of text ===
            if text is None:
                call_units = 1
            else:
                call_units = int(len(text) / 100 + 1)
            # =================================================

            increment_auth_token_call_count(auth_token, call_units,  # Count one API call per call unit.
                                            f.__name__)

            # promths_request_histogrm.labels(endpoint=f.__name__).observe(call_duration)  # pylint: disable=no-member
            promths_request_latency_gauge.labels(endpoint=f.__name__).set(call_duration)  # pylint: disable=no-member

            call_count, call_count_limit = auth_token_call_cache.get(auth_token, (0, None))
            # promths_call_units_histogrm.labels(endpoint=f.__name__).observe(call_units)  # pylint: disable=no-member
            promths_call_count_gauge_authrsd.labels(auth_desc=auth_desc).set(call_count)  # pylint: disable=no-member

            logging.info(f"cached_call_count = {auth_token_call_cache.get(auth_token)}, "
                         f"cached_desc = {auth_desc}, caller_name = {caller_name}")

        last_operation_end_time = time.time()

        return response_code, response_json

    return decorated_f


def load_model_history(name: str,
                       history_size: int) -> List[Dict]:
    """
    Get the recent history of this model.

    :param name: The name of the model e.g. "my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a.text_clsfr_meta_pickle"
    :param history_size: The max number of history items to return.
    :return: Model history list of json - List[{version, uuid, message}]]
    """
    query = db.session.query(WrapperBlobDataVersioned)

    query = query.options(load_only("version", "uuid", "message"))

    query = query.filter_by(name=name)
    query = query.order_by(WrapperBlobDataVersioned.version.desc())

    db_model_list = query.limit(history_size).all()

    model_history = []  # type: List[Dict]

    for instance in db_model_list:
        model_history.append(
            {
                "version": instance.version,
                "uuid": instance.uuid,
                "message": instance.message
            })

    db.session.close()

    return model_history


def load_model_list(auth_token: str,
                    show_data_objects: Optional[bool]) -> List[Tuple[str, str, bool, Optional[str], Optional[str]]]:
    """
    Get the list of models stored in the DB for this auth_token.

    :param auth_token: The auth token to get the model list for.
    :param show_data_objects: Set to True to include the data_objects in the dash_board response. Default is False.
    :return: List[Tuple[name, uuid, trashed, desc, long_name]]
    """
    query = db.session.query(WrapperBlobData)

    # ToDo: A good performance improvement here would be to also have the desc and long_name
    #   as table columns (instead of just in the blob) so that one might only need to do:
    # query = query.options(load_only("uuid", "trashed", "desc"))

    query = query.filter(WrapperBlobData.name.like("%_{}.%".format(auth_token)))

    db_model_list = query.all()

    model_info_list = []  # type: List[Tuple[str, str, bool, Optional[str], Optional[str]]]

    for instance in db_model_list:
        try:
            handle = io.BytesIO(instance.blob)
            meta_info = pickle.load(handle)
            handle.close()

            if isinstance(meta_info, DataObjectMeta):
                # DataObjectMeta doesn't have fields like 'desc' and 'long_name'.
                if show_data_objects is True:
                    model_info_list.append((instance.name, instance.uuid, instance.trashed,
                                            None, None))
            else:
                model_info_list.append((instance.name, instance.uuid, instance.trashed,
                                        meta_info.desc, meta_info.long_name))
        except AttributeError as e:
            logging.error(f"wrapper_util.load_model_list: AttributeError {e}")

    db.session.close()

    return model_info_list


def load_model_meta_info_list(auth_token: str) -> List[Tuple[str, Any]]:
    """
    Get the meta info for each object stored in the DB for this auth_token.

    :param auth_token: The auth token to get the model meta info list for.
    :return: List[Tuple[name, meta_info object]]
    """
    query = db.session.query(WrapperBlobData)
    query = query.filter(WrapperBlobData.name.like("%_{}.%".format(auth_token)))

    # ToDo: A good performance improvement here would be to optionally filter by model type (optional param) because this
    #  method is typically used for `_get_details_all` of certain model type!

    db_model_list = query.all()

    model_meta_info_list = []

    for instance in db_model_list:
        try:
            handle = io.BytesIO(instance.blob)
            meta_info = pickle.load(handle)
            handle.close()

            model_meta_info_list.append((instance.name, meta_info))
        except AttributeError as e:
            logging.error(f"wrapper_util.load_model_meta_info_list: AttributeError {e}")

    db.session.close()

    return model_meta_info_list


def add_auth_token(auth_token: str, desc: Optional[str],
                   call_count_limit: Optional[int] = None,
                   call_count_limit_relative: bool = False) -> bool:
    """
    Add or update an auth token to the DB. Local cache will be updated during next API request in is_auth_token_valid(...)!

    :param auth_token: The auth token to add/update.
    :param desc: The description to apply to the token. 'None' to leave existing description unchanged.
    :param call_count_limit: The call count limit to place on the token. 'None' to make unlimited.
    :param call_count_limit_relative: If True then the limit will be relative to the current count. Default is False!
    :return: True/False indicating success of operation.
    """
    try:
        query = db.session.query(APIKeyData)
        instance = query.get(ident=auth_token)

        if instance:
            if desc is not None:
                instance.desc = desc

            # Initialise the call_count if None.
            if instance.call_count is None:
                instance.call_count = 0

            if (call_count_limit is None) or (call_count_limit_relative is False):
                instance.call_count_limit = call_count_limit
            else:
                instance.call_count_limit = instance.call_count + call_count_limit
        else:
            instance = APIKeyData(auth_token, str(desc), 0, call_count_limit)
            db.session.add(instance)

        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def remove_auth_token(auth_token: str) -> bool:
    """
    Removes an auth token.

    :param auth_token: The auth token to remove.
    :return: True/False indicating success of operation.
    """
    try:
        query = db.session.query(APIKeyData)
        instance = query.get(ident=auth_token)

        if instance:
            db.session.delete(instance)
            db.session.commit()
            success = True
        else:
            success = False

        # Remove breakdown call counts for this auth token.
        query = db.session.query(APICallCountBreakdownData)
        rows = query.filter_by(auth_key=auth_token).all()

        if rows:
            for row in rows:
                db.session.delete(row)
            db.session.commit()

        return success
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def load_auth_token_list() -> List[str]:
    """
    Get the list of auth tokens stored in the DB.

    :return: List[str]
    """
    query = db.session.query(APIKeyData)
    query = query.options(load_only("auth_key"))

    api_key_object_list = query.all()
    auth_token_list = []

    for instance in api_key_object_list:
        auth_token_list.append(instance.auth_key)

    db.session.close()

    return auth_token_list


def get_auth_token_details(auth_token: str) -> Optional[Dict]:
    """
    Gets the desc, call_count and call_count_limit of an auth token.

    :param auth_token: The auth token to get the details of.
    :return: None if auth token not found, else {desc, call_count, call_count_limit}
    """
    query = db.session.query(APIKeyData)
    instance = query.get(ident=auth_token)

    auth_token_details = None  # type: Optional[Dict]

    if instance:
        desc = instance.desc
        call_count = instance.call_count
        call_count_limit = instance.call_count_limit

        if call_count is None:
            call_count = 0

        auth_token_details = {"desc": desc,
                              "call_count": call_count,
                              "call_count_limit": call_count_limit}

        # Get call count breakdown.
        query = db.session.query(APICallCountBreakdownData)
        rows = query.filter_by(auth_key=auth_token).all()

        if rows:
            breakdown_dict = {}
            for row in rows:
                breakdown_dict[row.endpoint] = row.call_count
            auth_token_details['call_count_breakdown'] = breakdown_dict

    db.session.close()
    return auth_token_details


def add_admin_auth_token(auth_token: str, desc: str) -> bool:
    """ Add or update an admin auth_token to the DB. """
    try:
        query = db.session.query(AdminAPIKeyData)
        instance = query.get(ident=auth_token)

        if instance:
            instance.desc = desc
        else:
            instance = AdminAPIKeyData(auth_token, desc)
            db.session.add(instance)

        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def remove_admin_auth_token(auth_token: str) -> bool:
    """
    Removes an admin auth token.

    :param auth_token: The auth token to remove.
    :return: True/False indicating success of operation.
    """
    try:
        query = db.session.query(AdminAPIKeyData)
        instance = query.get(ident=auth_token)

        if instance:
            db.session.delete(instance)
            db.session.commit()
            success = True
        else:
            success = False

        return success
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def load_admin_auth_token_list() -> List[str]:
    """
    Get the list of adminauth tokens stored in the DB.

    :return: List[str]
    """
    query = db.session.query(AdminAPIKeyData)
    query = query.options(load_only("auth_key"))

    api_key_object_list = query.all()
    auth_token_list = []

    for instance in api_key_object_list:
        auth_token_list.append(instance.auth_key)

    db.session.close()

    return auth_token_list


def add_default_auth_tokens():
    """ Add some known auth tokens to the DB for ease of dev and use. """
    add_admin_auth_token('FEERSUM-NLU-591-4ba0-8905-996076e94d', "Admin & Testing.")
    add_auth_token('FEERSUM-NLU-591-4ba0-8905-996076e94d', "Admin & Testing.")
    add_auth_token('ac13bedb-01be-4130-9a68-00e21fb4a111', 'pingdom')

    add_auth_token('FEERSUM-NLU-431-9020-80dd-cec15695d7', "Playground")
    add_auth_token('8e576a56-5f88-4c82-b0dd-ed5a455094f7', "Bernardt dev")
    add_auth_token('ab38db33-aa04-4d35-8ef1-4ade23e99fc2', "Ari dev")
    add_auth_token('75cba323-f567-46a9-a496-6d07a8dea1c8', 'Colin dev')
    add_auth_token('c22c6f1b-93e9-42d1-a916-30fa66fa72e0', "Feersum dev")
    add_auth_token('f6e8286f-3fee-4e0d-b847-0ca1241d2c00', "Feersum test")
    add_auth_token('PKD-bc7a-6a1d-4c3d-b052-c590941470c8', "Praekelt dev")
    add_auth_token('49888c27-54b8-44f0-a154-861234e9f437', "Feersum Generic Models")

    add_auth_token('f2da2d23-7dcb-4aa9-b3fe-6842fdfcb2d1', "lingua")
    add_auth_token('f2da2d23-7dcb-4aa9-b3fe-6842fdfcb-QA', "lingua-QA")

    # ToDo: The default tokens is for ease of use and dev and should really be limited to only dev/admin/trusted parties
    # like above, but NOT LIKE below!
    # ToDo: The below tokens should really be managed by Lasso or some other system via NLU token API.

    # === User tokens ===
    # add_auth_token('AM-316b3-259b-421e-8ffb-6b9b4b32157d', "Matt Arderne")
    # add_auth_token('GR-ad035-17f5-4895-b4ed-f738f565fc74', "Luke Jordan / Grass Roots")
    # add_auth_token('MA-15d55-a6a5-42a8-be67-e59a96afd5de', "a.moerat84@gmail.com")
    # add_auth_token('SL-c69fa-43ea-40fb-a740-1a636fe57d63', "lindo.shongwe@khasaniconsulting.co.za")
    # add_auth_token('88094ee9-141c-4702-8ef8-912c3ff553e6', "Dallas Goldswain")
    # add_auth_token('00af13cf-14fc-4fc2-a9fc-e2bb12aaabcf', "FNB")
    # add_auth_token('e6188738-253e-4960-9ab6-cf82711d383a', "Mark Jones JNSMAR043@myuct.ac.za")

    add_auth_token('MomConnect-1e-4315-bf7c-ea7d1aa25b55', "MomConnect")
    add_auth_token('MomConnect-1e-4315-bf7c-ea7d1aa25-QA', "MomConnect-QA")

    add_auth_token('e329a0be-dc8d-4128-b424-59e4cf429e46', "Massmart")
    add_auth_token('e329a0be-dc8d-4128-b424-59e4cf429-QA', "Massmart-QA")

    add_auth_token('4cf1e71a-7ee7-4a6e-8c2a-02f85b16832d', "MTN")
    add_auth_token('4cf1e71a-7ee7-4a6e-8c2a-02f85b168-QA', "MTN-QA")

    add_auth_token('921812c5-d77d-4f71-9524-e205998af871', "PharmaDynamics")
    add_auth_token('921812c5-d77d-4f71-9524-e205998af-QA', "PharmaDynamics-QA")

    add_auth_token('b2606e67-8341-4371-82e3-83fafd87ce6d', "DSTV")
    add_auth_token('b2606e67-8341-4371-82e3-83fafd87c-QA', "DSTV-QA")

    # add_auth_token('47e038bb-9bf2-4d7f-adbf-d681ddaeba40', "BCX")
    # add_auth_token('47e038bb-9bf2-4d7f-adbf-d681ddaeb-QA', "BCX-QA")

    # add_auth_token('d85311c1-ad2b-440f-95a8-09be96713ea0', "Daniel Lotz")
    # add_auth_token('e0ab0361-c397-4737-ad1f-d14d2e91fd7c', "Kgosi Matome")
    # add_auth_token('2707cee1-e4f9-4880-a99e-b9ed5303a176', "carla@zelda.org.za")
    # add_auth_token('724661ac-1fe8-44a4-85dc-a0f77c72a127', "tshepo@4digits.co.za")
    # add_auth_token('fe77af7a-7ed4-4500-9c58-6db92f6fdaef', "Carbon Black")
    # add_auth_token('1d63c08f-dd82-4b81-9823-0c2e8a3f105f', "Byte Money")
    # add_auth_token('591065fc-aac9-4467-8cc1-1289f213f5f0', "Francesca from Udacity DLND")

    add_auth_token('6847a0a3-169d-4f7a-8eb1-737c9f6e9ffd', "Vicci.ai")
    add_auth_token('6847a0a3-169d-4f7a-8eb1-737c9f6e9-QA', "Vicci.ai-QA")

    add_auth_token('5c9bcc0c-b103-4ce2-9060-634b903c0dc5', 'Vicci.ai2')
    add_auth_token('5c9bcc0c-b103-4ce2-9060-634b903c0-QA', 'Vicci.ai2-QA')

    add_auth_token('3c17440f-6ade-46d3-816b-fff5bde117cb', "EVO")
    add_auth_token('3c17440f-6ade-46d3-816b-fff5bde11-QA', "EVO-QA")

    add_auth_token('4504644e-ad0f-473a-b88d-8ab47f088765', "Solved")
    add_auth_token('4504644e-ad0f-473a-b88d-8ab47f088-QA', "Solved-QA")

    add_auth_token('12053bf8-1b61-4b33-9c53-1ffb3a419a54', "Remedy")
    add_auth_token('12053bf8-1b61-4b33-9c53-1ffb3a419-QA', "Remedy-QA")

    add_auth_token('6aa6a5f3-7318-421f-9ef2-d3ddbbc22e62', 'ithuba')
    add_auth_token('6aa6a5f3-7318-421f-9ef2-d3ddbbc22-QA', 'ithuba-QA')

    add_auth_token('01b7642e-3449-4166-b435-6d547dbdc579', 'Tumi')
    add_auth_token('01b7642e-3449-4166-b435-6d547dbdc-QA', 'Tumi-QA')

    add_auth_token('d93af212-ab33-42de-b2a8-30bddd918476', 'tkn025')
    add_auth_token('4b06e626-b5c4-410b-a420-9747671e506b', 'tkn027')
    add_auth_token('8283b535-1e63-4fa9-9930-4903300ff5c2', 'tkn028')
    add_auth_token('e77613ab-4c83-47ee-8c05-6699efa3ddf6', 'tkn029')
    add_auth_token('e4dbf2e1-f081-45ee-bd64-398aa0827a57', 'tkn030')
    add_auth_token('5f6e0d9d-aa68-43c5-9c8b-3ef4c28a5235', 'tkn031')
    add_auth_token('d72dcaaa-d804-4f7f-9da4-2b918bf751fa', 'tkn032')
    add_auth_token('cd889fd8-82bc-4004-be7f-625d97349dc8', 'tkn033')
    add_auth_token('f3d116aa-0688-4061-86c9-55f00993d185', 'tkn034')
    add_auth_token('20029082-6cc5-41ba-b8e7-493f912d7459', 'tkn035')
    add_auth_token('13ad6024-6ba8-47c3-90ee-20ed728e9d13', 'tkn036')
    add_auth_token('36b9b566-afbb-45df-8970-95fd6490fc60', 'tkn037')
    add_auth_token('e3283409-650f-4f1a-84da-bf2c38cd28de', 'tkn038')
    add_auth_token('6bc8ac10-8c35-4ec2-8ef0-b2c54a92c12b', 'tkn039')


def is_auth_token_valid(auth_token: str) -> bool:
    """
    Checks if the auth token is a valid token and that its rate limit has not been exceeded. Also
    updates the local call count and API key desc caches with the info from the DB.

    :param auth_token: The auth token.
    :return: True only if the token is a valid token and its rate limit has not been exceeded.
    """

    global __default_auth_tokens_configured

    try:
        # Check if the default tokens have been initialised.
        if not __default_auth_tokens_configured:
            add_default_auth_tokens()
            __default_auth_tokens_configured = True

        query = db.session.query(APIKeyData)
        # query = query.options(load_only("auth_key", "desc", "call_count", "call_count_limit"))

        instance = query.get(ident=auth_token)

        # 1 - Initialise call_count if None.
        if instance and instance.call_count is None:
            # Token valid, but call_count not assigned yet.
            instance.call_count = 0
            db.session.commit()

        # 2 - Update the local call count cache which is updated and used later to build response headers, etc.
        if instance:
            auth_token_call_cache[auth_token] = (instance.call_count, instance.call_count_limit)
            auth_token_desc_cache[auth_token] = instance.desc
        else:
            auth_token_call_cache.pop(auth_token, None)
            auth_token_desc_cache.pop(auth_token, None)

        # 3 - Check that token is valid and rate limit (if any) not exceeded.
        if instance and \
                ((instance.call_count_limit is None) or
                 (instance.call_count < instance.call_count_limit)):
            # Token valid AND (no rate limit OR rate limit not exceeded).
            valid = True
        else:
            valid = False

        return valid
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def increment_auth_token_call_count(auth_token: str, units: int,
                                    endpoint: Optional[str] = None):
    """
    Increments the call count for the auth token - increments the DB and the local cache.

    :param auth_token: The auth token.
    :param units: The number of units of use.
    :param endpoint: The endpoint to allocate the call count to.
    """
    try:
        # Atomic update of call_count in DB.
        query = db.session.query(APIKeyData)
        query.filter_by(auth_key=auth_token).update({'call_count': APIKeyData.call_count + units})
        db.session.commit()

        # Update of the local call cache.
        cached_call_count_tuple = auth_token_call_cache.get(auth_token)
        if cached_call_count_tuple is not None:
            auth_token_call_cache[auth_token] = (cached_call_count_tuple[0] + units, cached_call_count_tuple[1])

        if endpoint is not None:
            # Atomic update of call count breakdown in DB.
            query = db.session.query(APICallCountBreakdownData)
            row_count = \
                query.filter_by(auth_key=auth_token,
                                endpoint=str(endpoint)
                                ).update({'call_count': APICallCountBreakdownData.call_count + units})

            if row_count == 0:
                # Add the key,endpoint row if not yet present.
                instance = APICallCountBreakdownData(auth_token, endpoint, units)
                db.session.add(instance)

            db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def is_admin_auth_token_valid(auth_token: str) -> bool:
    global __default_auth_tokens_configured

    # Check if the default tokens have been initialised.
    if not __default_auth_tokens_configured:
        add_default_auth_tokens()
        __default_auth_tokens_configured = True

    query = db.session.query(AdminAPIKeyData)
    query = query.options(load_only("auth_key"))

    instance = query.get(ident=auth_token)

    if instance:
        valid = True
    else:
        valid = False

    db.session.close()
    return valid


def load_meta_info_blob_from_history(revision_uuid: Optional[str]) -> Optional[Any]:
    """ Try to load model meta data from the storage system.  Returns the blob. """
    try:
        query = db.session.query(WrapperBlobDataVersioned)
        instance = query.filter_by(uuid=revision_uuid).first()

        if instance is not None:
            handle = io.BytesIO(instance.blob)
            logging.info(f"load_meta_info_blob_from_history: Loading {revision_uuid} from instance.blob.")
            meta_blob = pickle.load(handle)
            handle.close()
        else:
            logging.info(f"load_meta_info_blob_from_history: {revision_uuid} not found!")
            meta_blob = None
    except IOError as e:
        logging.error(f"wrapper_util.load_meta_info_blob_from_history: {revision_uuid} IOError {e}!")
        meta_blob = None
        db.session.rollback()
    except AttributeError as e:
        logging.error(f"wrapper_util.load_meta_info_blob_from_history: AttributeError {e}")
        meta_blob = None
        db.session.rollback()
    finally:
        db.session.close()

    return meta_blob


def load_meta_info_blob(name: str,
                        look_in_trash: bool,
                        cached_meta_blob: Optional[Any]) -> Optional[Any]:
    """ Try to load model meta data from the storage system.  Returns the blob. """

    # ToDo [Possible performance improvement] - If needed then the cached blob can be returned only once every few ms for
    #  retrieve requests and whenever the blob just needs to be read.
    try:
        query = db.session.query(WrapperBlobData)

        if cached_meta_blob is not None:
            # Make a new query that just returns the uuid and trashed columns to check if the cached_meta_blob is fresh.
            query = query.options(load_only("uuid", "trashed"))
            instance_is_partial = True
        else:
            instance_is_partial = False

        instance = query.get(ident=name)

        if (instance is not None) and ((not instance.trashed) or look_in_trash):
            # === Get meta_blob (either from the instance or from the cache) ===
            if (cached_meta_blob is not None) and (cached_meta_blob.uuid == instance.uuid):
                # UUID of cache is same as DB instance so reuse cached value.

                meta_blob = cached_meta_blob
            else:
                # UUID of DB instance is fresh or cached_meta_blob is None so get full object from DB.

                if instance_is_partial:
                    # Get full object
                    query = db.session.query(WrapperBlobData)
                    instance = query.get(ident=name)

                handle = io.BytesIO(instance.blob)

                # if cached_meta_blob is None:
                #     logging.info(f"    load_meta_info_blob: Loading {name} from instance.blob (cache none).")
                # else:
                #     logging.info(f"    load_meta_info_blob: Loading {name} from instance.blob (cache was stale).")

                meta_blob = pickle.load(handle)
                handle.close()
            # === ===

            if instance.trashed:
                # Un-trash if found in the trash.
                instance.trashed = False
                db.session.commit()
        else:
            logging.info(f"    load_meta_info_blob: {name} in trash or not found!")
            meta_blob = None

    except IOError as e:
        logging.error(f"wrapper_util.load_meta_info_blob: {name} IOError {e}!")
        meta_blob = None
        db.session.rollback()
    except AttributeError as e:
        logging.error(f"wrapper_util.load_meta_info_blob: AttributeError {e}")
        meta_blob = None
        db.session.rollback()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return meta_blob


class SaveHelperMode(Enum):
    VAPORISE_MODEL = 1
    SAVE_MODEL = 2
    DONT_SAVE_MODEL = 3


def save_meta_info_blob_to_history(name: str, meta_info: Any,
                                   message: Optional[str]) -> bool:
    """
    Try to save the model meta data to the revision control storage system.

    :param name: The name of the model e.g. "my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a.text_clsfr_meta_pickle"
    :param meta_info: The model's meta info.
    :param message: The message to be attached to this revision of the meta info.
    :return: True if save successful.
    """
    try:
        handle = io.BytesIO()
        logging.info(f"    save_meta_info_blob_in_history: Dumping {name} to blob.")
        pickle.dump(meta_info, handle, protocol=feersum_nlu_pickle_protocol_version)

        # Add the new version of the model to the DB. The version primary key should auto-increment.
        instance = WrapperBlobDataVersioned(_name=name, _blob=handle.getvalue(),
                                            _uuid=meta_info.uuid,
                                            _message=message)
        db.session.add(instance)

        handle.close()

        logging.info(f"    save_meta_info_blob_in_history: Committing {name} to DB.")

        db.session.commit()
        return True
    except IOError as e:
        logging.error(f"    save_meta_info_blob: {name} IOError {e}.")
        db.session.rollback()
        return False
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def save_meta_info_blob(name: str, meta_info: Any,
                        save_in_history: bool,
                        save_in_history_message: Optional[str]) -> bool:
    """ Try to save the model meta data to the storage system. """
    try:
        handle = io.BytesIO()
        # logging.info(f"    save_meta_info_blob: Dumping {name} to blob.")
        pickle.dump(meta_info, handle, protocol=feersum_nlu_pickle_protocol_version)

        instance = WrapperBlobData.query.get(ident=name)

        if instance:
            instance.blob = handle.getvalue()
            instance.uuid = meta_info.uuid  # Update the uuid in the DB with the blob's uuid.
            instance.trashed = False
        else:
            instance = WrapperBlobData(_name=name, _blob=handle.getvalue(),
                                       _uuid=meta_info.uuid, _trashed=False)
            db.session.add(instance)

        handle.close()

        # logging.info(f"    save_meta_info_blob: Committing {name} to DB.")

        db.session.commit()

        return True if not save_in_history else save_meta_info_blob_to_history(name, meta_info,
                                                                               message=save_in_history_message)
    except IOError as e:
        logging.error(f"    save_meta_info_blob: {name} IOError {e}.")
        db.session.rollback()
        return False
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def trash_meta_info_blob(name: str) -> bool:
    """ Mark the blob as trashed in the storage system. """
    try:
        instance = WrapperBlobData.query.get(ident=name)

        if instance:
            instance.trashed = True
            db.session.commit()
            success = True
        else:
            success = False

        return success
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def vaporise_meta_info_blob(name: str) -> bool:
    """ Permanently delete the blob from the storage system. """
    try:
        instance = WrapperBlobData.query.get(ident=name)

        if instance:
            db.session.delete(instance)
            db.session.commit()
            success = True
        else:
            success = False

        return success
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def is_string(obj):
    """ Helper type checker function. """
    return isinstance(obj, str)


def is_list_of_strings(lst):
    """ Helper type checker function. """
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False


def load_shared_models(lm_name_list: Iterable[str],
                       vm_name_list: Iterable[str]):
    """
    Load the models that are shared amongst all the tenants for this instance. Shared models that are not pre-loaded
    will be lazy loaded as used. Always loads at least nlp_engine.feers_sent_encoder_default!

    :return: None
    """
    start_time = time.time()
    print("Creating the requested shared models .....")
    print('[Feersum NLU version = ' + nlp_engine.get_version() + ']')
    print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']')

    logging.info(f"load_shared_models: Loading the shared language models .....")

    get_nlpe_engine().create_feers_language_model(nlp_engine.feers_sent_encoder_default)

    for name in lm_name_list:
        get_nlpe_engine().create_feers_language_model(name)

    for name in vm_name_list:
        get_vision_engine().create_feers_vision_model(name)

    end_time = time.time()
    print('Done in ' + str(end_time - start_time) + "s")
    print()

    logging.info(f"load_default_models: done loading shared language models.")
