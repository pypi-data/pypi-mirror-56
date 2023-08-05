"""
FeersumNLU's Celery tasks. The tasks should all call back to wrapper functions!
"""

from typing import Tuple, Dict, Optional, Union, Any, List
from celery import shared_task

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


@shared_task(ignore_result=True)
def faq_train(iname: str, auth_token: str,
              weak_match_threshold: Optional[float],
              requested_word_manifold_dict: Optional[Dict[str, str]],
              callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.faq_wrapper import _faq_train_impl  # noqa

    return _faq_train_impl(iname, auth_token, weak_match_threshold,
                           requested_word_manifold_dict,
                           callback_url)


@shared_task(ignore_result=True)
def faq_tsne_post(iname: str, auth_token: str,
                  n_components: int, perplexity: float, learning_rate: float,
                  callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.faq_wrapper import _faq_tsne_post_impl  # noqa

    return _faq_tsne_post_impl(iname, auth_token,
                               n_components, perplexity, learning_rate,
                               callback_url)


@shared_task(ignore_result=True)
def intent_clsfr_train(iname: str, auth_token: str,
                       weak_match_threshold: Optional[float],
                       requested_word_manifold_dict: Optional[Dict[str, str]],
                       callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.intent_wrapper import _intent_clsfr_train_impl  # noqa

    return _intent_clsfr_train_impl(iname, auth_token, weak_match_threshold,
                                    requested_word_manifold_dict,
                                    callback_url)


@shared_task(ignore_result=True)
def intent_clsfr_tsne_post(iname: str, auth_token: str,
                           n_components: int, perplexity: float, learning_rate: float,
                           callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.intent_wrapper import _intent_clsfr_tsne_post_impl  # noqa

    return _intent_clsfr_tsne_post_impl(iname, auth_token,
                                        n_components, perplexity, learning_rate,
                                        callback_url)


@shared_task(ignore_result=True)
def text_clsfr_train(iname: str, auth_token: str,
                     weak_match_threshold: Optional[float],
                     clsfr_algorithm: Optional[str],
                     requested_language_model_dict: Optional[Dict[str, str]],
                     callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.text_classifier_wrapper import _text_clsfr_train_impl  # noqa

    return _text_clsfr_train_impl(iname, auth_token, weak_match_threshold,
                                  clsfr_algorithm, requested_language_model_dict,
                                  callback_url)


@shared_task(ignore_result=True)
def text_clsfr_tsne_post(iname: str, auth_token: str,
                         n_components: int, perplexity: float, learning_rate: float,
                         callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.text_classifier_wrapper import _text_clsfr_tsne_post_impl  # noqa

    return _text_clsfr_tsne_post_impl(iname, auth_token,
                                      n_components, perplexity, learning_rate,
                                      callback_url)


@shared_task(ignore_result=True)
def image_clsfr_train(iname: str, auth_token: str,
                      weak_match_threshold: Optional[float],
                      clsfr_algorithm: Optional[str],
                      num_epochs: Optional[int],
                      callback_url: Optional[str]) -> Tuple[int, JSONType]:
    # Prevent circular import
    from feersum_nlu.rest_api.image_classifier_wrapper import _image_clsfr_train_impl  # noqa

    return _image_clsfr_train_impl(iname, auth_token, weak_match_threshold,
                                   clsfr_algorithm,
                                   num_epochs,
                                   callback_url)
