# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_request, check_response_test
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestFAQ(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_faq_matcher(self):
        print("Rest HTTP test_faq_matcher:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1', 'get',
                                       {},
                                       400,
                                       {
                                           'error_detail': 'Named instance faq1 not loaded!'
                                       }))

        # Test create.
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

        training_samples = [
            {
                "label": "The SDK is written in Python.",
                "text": "In what programming language is the SDK written?"
            },
            {
                "label": "The engine has Python and HTTP REST interfaces.",
                "text": "What application interfaces are supported?"
            },
            {
                "label": "The SDK was created by the Feersum.io team.",
                "text": "Who created the SDK?"
            }
        ]

        testing_samples = [
            {
                "label": "The SDK is written in Python.",
                "text": "In what language was the SDK developed?"
            },
            {
                "label": "The engine has Python and HTTP REST interfaces.",
                "text": "What development interfaces are supported?"
            },
            {
                "label": "The SDK was created by the Feersum.io team.",
                "text": "Which team developed the SDK?"
            }
        ]

        # Add some training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples',
                                       'post',
                                       training_samples,
                                       200,
                                       training_samples
                                       ))

        # Add some testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/testing_samples', 'post',
                                       testing_samples,
                                       200,
                                       testing_samples
                                       ))

        #####
        # Test retrieve when not yet trained.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       200,
                                       []))

        # Test train and save of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/train',
                                       'post',
                                       {
                                           "immediate_mode": True,
                                           "threshold": 0.75,
                                           "word_manifold_list": [
                                               {
                                                   "label": "eng",
                                                   "word_manifold": "glove6B50D_trimmed"
                                               }
                                           ]
                                       },
                                       200,
                                       {'cm_labels': {'0': 'The SDK is written in Python.',
                                                      '1': 'The engine has Python and HTTP REST interfaces.',
                                                      '2': 'The SDK was created by the Feersum.io team.', '_nc': '_nc'},
                                        'desc': 'FAQ Matcher for the Feersum NLU SDK.',
                                        'lid_model_file': 'lid_za',
                                        'long_name': None, 'name': 'faq1', 'num_testing_samples': 3,
                                        'num_training_samples': 3, 'readonly': False, 'testing_accuracy': 1.0,
                                        'testing_cm': {'0': {'0': 1}, '1': {'1': 1}, '2': {'2': 1}}, 'testing_f1': 1.0,
                                        'threshold': 0.75, 'training_accuracy': 1.0,
                                        'training_cm': {'0': {'0': 1}, '1': {'1': 1}, '2': {'2': 1}}, 'training_f1': 1.0,
                                        'validation_accuracy': 0.0,
                                        'validation_cm': {}, 'validation_f1': 0.0,
                                        'word_manifold_list': [{'label': 'eng', 'word_manifold': 'glove6B50D_trimmed'}]
                                        }))

        # Test delete of single training sample.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples', 'delete',
                                       [
                                           training_samples[1]
                                       ],
                                       200,
                                       [
                                           training_samples[1]
                                       ]))

        # Test delete of training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples_all', 'delete',
                                       {},
                                       200,
                                       [
                                           training_samples[0],
                                           training_samples[2]
                                       ],
                                       treat_list_as_set=True))

        # Add training samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples',
                                       'post',
                                       training_samples,
                                       200,
                                       training_samples))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       200,
                                       [
                                           {
                                               'label': 'The SDK is written in Python.',
                                               'probability': 0.9631024203073986
                                           }
                                       ]))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1', 'delete',
                                       {},
                                       200,
                                       {
                                           "name": "faq1"
                                       }))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers', 'post',
                                       {
                                           "name": "faq1",
                                           "load_from_store": True
                                       },
                                       200,
                                       {
                                           "name": "faq1"
                                       }))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1', 'get',
                                       {},
                                       200,
                                       {
                                           "desc": "FAQ Matcher for the Feersum NLU SDK.",
                                           "name": "faq1",
                                           'cm_labels': {'0': 'The SDK is written in Python.',
                                                         '1': 'The engine has Python and HTTP REST interfaces.',
                                                         '2': 'The SDK was created by the Feersum.io team.', '_nc': '_nc'}
                                       }))

        # Test get training data.
        response = check_response_request(self.client,
                                          '/nlu/v2/faq_matchers/faq1/training_samples', 'get',
                                          {})
        self.assertTrue(check_response_test(response,
                                            200,
                                            training_samples,
                                            treat_list_as_set=True))

        uuid_to_delete = response.json[1]['uuid']
        sample_to_delete = response.json[1]

        # Test delete of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples', 'delete',
                                       [{"uuid": uuid_to_delete}],
                                       200,
                                       [{'label': 'The engine has Python and HTTP REST interfaces.',
                                         'uuid': uuid_to_delete}],
                                       treat_list_as_set=True))

        # Add training samples back (ignoring duplicates).
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/training_samples', 'post',
                                       training_samples,
                                       200,
                                       [{'label': sample_to_delete['label'], 'text': sample_to_delete['text']}],
                                       treat_list_as_set=True))

        # Test get testing data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/testing_samples',
                                       'get',
                                       {},
                                       200,
                                       testing_samples))

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       200,
                                       [
                                           {
                                               'label': 'The SDK is written in Python.',
                                               'probability': 0.9631024203073986
                                           }
                                       ]))

        # Test the TSNE calculation - start the task.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/tsne',
                                       'post',
                                       {
                                           "n_components": 3,
                                           "perplexity": 35,
                                           "learning_rate": 250
                                       },
                                       200,
                                       {},
                                       ))

        time.sleep(5)

        # Test the TSNE calculation - Get the results.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/tsne',
                                       'get',
                                       {},
                                       200,
                                       [{'label': 'The SDK is written in Python.',
                                         'text': 'In what programming language is the SDK written?'},
                                        {'label': 'The engine has Python and HTTP REST interfaces.',
                                         'text': 'What application interfaces are supported?'},
                                        {'label': 'The SDK was created by the Feersum.io team.',
                                         'text': 'Who created the SDK?'}],
                                       treat_list_as_set=True))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        faq_meta_info = wrapper_util.faq_dict.get('faq1_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(faq_meta_info is not None)
        if faq_meta_info is not None:
            faq_meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       200,
                                       [
                                           {
                                               'label': 'The SDK is written in Python.',
                                               'probability': 0.9631024203073986
                                           }
                                       ]))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {},
                                       400,
                                       {
                                           "detail": "'text' is a required property"
                                       }))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1', 'delete',
                                       {},
                                       200,
                                       {
                                           "name": "faq1"
                                       }))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/faq_matchers/faq1/retrieve',
                                       'post',
                                       {
                                           "text": "Was the SDK programmed in C++?"
                                       },
                                       400,
                                       {
                                           'error_detail': 'Named instance faq1 not loaded!'
                                       }))

        print('time = ' + str(time.time() - start_time))
        print()
