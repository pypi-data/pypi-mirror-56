"""
Feersum_nlu LID.

Feersum_nlu LID based on a Naive Bayes text classifier with character ngram features. The labels should be the ISO-639-2
language codes e.g. eng, afr, nbl, xho, zul, ssw, nso, sot, tsn, ven, tso
"""

from typing import Tuple, List, Set  # noqa # pylint: disable=unused-import
import pickle
import logging
import re

from feersum_nlu import engine_utils
from feersum_nlu import nlp_engine_data

# === Accomodate unpickling, etc. of modules that have changed path ===#
# import sys
# from feersum_nlu.models import text_classifier_legacy

# sys.modules['feersum_nlu.models.text_classifier'] = text_classifier_legacy
# === === #

# ISO-639-2 codes like eng, afr, nbl, xho, zul, ssw, nso, sot, tsn, ven, tso.
lid_hints = {  # ToDo: Keep adding short words like greetings.
    r"\bhello\b": "eng",
    r"\bhi\b": "eng",
    r"\bhowzit\b": "eng",
    r"\bhowsit\b": "eng",
    r"\bgreet\b": "eng",
    r"\byes yes\b": "eng",
    r"\bgood day\b": "eng",
    r"\bgood morning\b": "eng",
    r"\bmorning\b": "eng",
    r"\bgood afternoon\b": "eng",
    r"\bgood evening\b": "eng",
    r"\bhoesit\b": "eng",
    r"\bgoeie dag\b": "afr",
    r"\bdag\b": "afr",
    r"\bgoeie môre\b": "afr",
    r"\bmôre\b": "afr",
    r"\bhallo\b": "afr",
    r"\bdumelang\b": "nso",
    r"\ble kae\b": "nso",
    r"\bo kae\b": "nso",
    r"\bahee\b": "sot",
    r"\bmolo\b": "xho",
    r"\bmolweni\b": "xho",
    r"\bunjani\b": "xho",
    r"\bninjani\b": "xho",
    r"\bmehlo madala\b": "xho",
    r"\bsawubona\b": "zul",
    r"\bsanibonani\b": "zul",
    r"\bongc' inde\b": "zul"
}


def load_lid_clsfr():
    # ToDo: Make the lid text classifier configurable?
    # Same load_text_clsfr code as in NLPEngine

    # filename = nlp_engine_data.get_path() + '/' + 'lid_za' + '.text_clsfr_pickle'
    local_file_cache_path, blob_file_name = \
        nlp_engine_data.get_blob_from_gcp_bucket("lid", 'lid_za.text_clsfr_pickle')
    filename = f"{local_file_cache_path}/{blob_file_name}"

    try:
        handle = open(filename, 'rb')
        lid_clsfr = pickle.load(handle)
        handle.close()
        return lid_clsfr
    except IOError:
        logging.error("    load_lid_clsfr: _lid_clsfr load error!")
        return None


# Load the LID text classifier model when this module is imported.
# ToDo: Fix this so that the model is loaded with the other pre-trained models (like the language models).
print("models.lid: Loading default LID model ...", end='', flush=True)
_lid_clsfr = load_lid_clsfr()
print("done.")


def get_labels():
    return _lid_clsfr.get_labels()


def lang_ident_nbayes(input_text: str) -> List[Tuple[str, float]]:
    """ Retrieve the language that the input text is written in.

    :param input_text: Document/Sentence to analyse.
    :return: Probable ISO-639-2 language code.
    """
    result_list = []  # type: List[Tuple[str, float]]
    hint_match_set = set()  # type: Set[str]

    # === Test the input against the lid_hint regexs ===
    if len(input_text) <= 15:
        for hint_regex, lang_code in lid_hints.items():
            p = re.compile(hint_regex, re.IGNORECASE)

            if p.search(input_text) is not None:
                hint_match_set.add(lang_code)
    # === ===

    if len(hint_match_set) > 0:
        for hint_match in hint_match_set:
            result_list.append((hint_match, 1.0 / len(hint_match_set)))
    elif _lid_clsfr is not None:
        result_list, input_lang_code = _lid_clsfr.classify(input_text=engine_utils.cleanup_text(input_text),
                                                           lang_code_hint=None,
                                                           weak_match_threshold=1.0,
                                                           top_n=1000)

    return result_list
