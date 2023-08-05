# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import __version__ as feersum_nlu_sdk_version


# @unittest.skip("skipping during dev")
class TestRestDashboard(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_dashboard(self):
        print("Rest HTTP test_dashboard:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")
        wrapper_util.add_admin_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test create of Duckling extractor.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/duckling_entity_extractors', 'post',
                                       {
                                           "name": "duckling_extr",
                                           "long_name": "An example duckling info extractor.",
                                           "desc": "Example duckling extractor model.",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example duckling extractor model.',
                                           'long_name': 'An example duckling info extractor.',
                                           'name': 'duckling_extr'
                                       }))

        # Test create of FAQ.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers', 'post',
                                       {
                                           "name": "faq1",
                                           "desc": "FAQ Matcher for the Feersum NLU SDK.",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           "name": "faq1"
                                       }))

        # Test create of intent
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/intent_classifiers', 'post',
                                       {"name": "intent1",
                                        "desc": "Intent Clsfr for the Feersum NLU SDK.",
                                        "load_from_store": False},
                                       200,
                                       {"name": "intent1"}))

        # Test create of LR4.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/language_recognisers', 'post',
                                       {
                                           "name": "lid_example",
                                           "desc": "Example LID model.",
                                           "lid_model_file": "lid_za",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example LID model.',
                                           'lid_model_file': 'lid_za',
                                           'long_name': None,
                                           'name': 'lid_example'
                                       }))

        # Test create of person name extractor.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/person_name_entity_extractors', 'post',
                                       {
                                           "name": "person_name_extr",
                                           "long_name": "An example person name info extractor.",
                                           "desc": "Example person name extractor model.",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example person name extractor model.',
                                           'long_name': 'An example person name info extractor.',
                                           'name': 'person_name_extr'
                                       }))

        # Test create of regex extractor.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/regex_entity_extractors', 'post',
                                       {
                                           "name": "regex_extr",
                                           "long_name": "An example regular expression info extractor.",
                                           "desc": "Example regex extractor model.",
                                           "regex": r"(?P<license>"
                                                    r"([A-Z]{3}[ ]?[0-9]{3}[ ]?(GP|NW|MP|EC|L|NC|NW))|"
                                                    r"([A-Z]{2}[ ]?[0-9]{2}[ ]?[A-Z]{2}[ ]?(GP|NW|MP|EC|L|NC|NW)))",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example regex extractor model.',
                                           'long_name': 'An example regular expression info extractor.',
                                           'name': 'regex_extr'
                                       }))

        # Test create sim word extractor.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sim_word_entity_extractors', 'post',
                                       {
                                           "name": "sim_word_extr",
                                           "long_name": "An example sim word info extractor.",
                                           "desc": "Example sim word extractor model.",
                                           "similar_words": ['cat'],
                                           "threshold": 0.6,
                                           "word_manifold": "glove6B50D_trimmed",
                                           "load_from_store": False
                                       },
                                       200,
                                       {
                                           'desc': 'Example sim word extractor model.',
                                           "long_name": "An example sim word info extractor.",
                                           'name': 'sim_word_extr'
                                       }))

        # Test create of text classifier.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers', 'post',
                                       {"name": "user_act",
                                        "desc": "Text classifier to classify user actions requests.",
                                        "load_from_store": False},
                                       200,
                                       {"name": "user_act"}))

        # Test the dashboard response.
        dashboard_check = check_response(self.client, "/nlu/v2/dashboard", "get",
                                         {},
                                         200,
                                         {
                                             'api_version': feersum_nlu_sdk_version,
                                             'model_list': [
                                                 {
                                                     'desc': 'Example duckling extractor model.',
                                                     'long_name': 'An example duckling info extractor.',
                                                     'model_type': 'duckling_entity_extractor',
                                                     'collection_uri': '/duckling_entity_extractors',
                                                     'name': 'duckling_extr',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'FAQ Matcher for the Feersum NLU SDK.',
                                                     'long_name': None,
                                                     'model_type': 'faq_matcher',
                                                     'collection_uri': '/faq_matchers',
                                                     'name': 'faq1',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Generic pre-created date parser.',
                                                     'long_name': 'Generic date_parser.',
                                                     'model_type': 'date_parser',
                                                     'collection_uri': '/date_parsers',
                                                     'name': 'generic',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Generic pre-created sentiment detector.',
                                                     'long_name': 'Generic sentiment_detector.',
                                                     'model_type': 'sentiment_detector',
                                                     'collection_uri': '/sentiment_detectors',
                                                     'name': 'generic',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Small Stanford Glove Word Embedding for English',
                                                     'long_name': 'Small Stanford Glove Word Embedding for English',
                                                     'model_type': 'sentence_encoder',
                                                     'collection_uri': '/sentence_encoders',
                                                     'name': 'glove6B50D_trimmed',
                                                     'trashed': False,
                                                     'sentence_encoder_type': 'Glove WordManifold',
                                                 },
                                                 {
                                                     'desc': 'Intent Clsfr for the Feersum NLU SDK.',
                                                     'long_name': None,
                                                     'model_type': 'intent_classifier',
                                                     'collection_uri': '/intent_classifiers',
                                                     'name': 'intent1', 'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Example LID model.',
                                                     'long_name': None,
                                                     'model_type': 'language_recogniser',
                                                     'collection_uri': '/language_recognisers',
                                                     'name': 'lid_example',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Example person name extractor model.',
                                                     'long_name': 'An example person name info extractor.',
                                                     'model_type': 'person_name_entity_extractor',
                                                     'collection_uri': '/person_name_entity_extractors',
                                                     'name': 'person_name_extr',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Example regex extractor model.',
                                                     'long_name': 'An example regular expression info extractor.',
                                                     'model_type': 'regex_entity_extractor',
                                                     'collection_uri': '/regex_entity_extractors',
                                                     'name': 'regex_extr',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Example sim word extractor model.',
                                                     'long_name': 'An example sim word info extractor.',
                                                     'model_type': 'sim_word_entity_extractor',
                                                     'collection_uri': '/sim_word_entity_extractors',
                                                     'name': 'sim_word_extr',
                                                     'trashed': False
                                                 },
                                                 {
                                                     'desc': 'Text classifier to classify user actions requests.',
                                                     'long_name': None,
                                                     'model_type': 'text_classifier',
                                                     'collection_uri': '/text_classifiers',
                                                     'name': 'user_act',
                                                     'trashed': False
                                                 }],
                                             'service_name': 'FeersumNLU Service'
                                         },
                                         treat_list_as_set=True)

        self.assertTrue(dashboard_check)

        print('time = ' + str(time.time() - start_time))
