# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_request, check_response_test
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestTextClassifier(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_text_classifier(self):
        print("Rest HTTP test_text_classifier:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance user_act not loaded!'}))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers', 'post',
                                       {"name": "user_act",
                                        "desc": "Text classifier to classify user actions requests.",
                                        "load_from_store": False},
                                       200,
                                       {"name": "user_act"}))

        # Add some training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'post',
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "help question"
                                           },
                                           {
                                               "label": "menu_class",
                                               "text": "menu main"
                                           },
                                           {
                                               "label": "quit_class",
                                               "text": "quit exit"
                                           }
                                       ],
                                       200,
                                       [{'label': 'help_class', 'lang_code': '', 'text': 'help question'},
                                        {'label': 'menu_class', 'lang_code': '', 'text': 'menu main'},
                                        {'label': 'quit_class', 'lang_code': '', 'text': 'quit exit'}]
                                       ))

        # Add some testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/testing_samples', 'post',
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "please help me"
                                           },
                                           {
                                               "label": "menu_class",
                                               "text": "Take me to the menu"
                                           },
                                           {
                                               "label": "quit_class",
                                               "text": "please quit"
                                           }
                                       ],
                                       200,
                                       [{'label': 'help_class', 'lang_code': '', 'text': 'please help me'},
                                        {'label': 'menu_class', 'lang_code': '', 'text': 'Take me to the menu'},
                                        {'label': 'quit_class', 'lang_code': '', 'text': 'please quit'}]
                                       ))

        #####
        # Test retrieve when not yet trained.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/retrieve',
                                       'post',
                                       {"text": "Please take me to the main menu.",
                                        "lang_code": "eng"},
                                       200,
                                       []))

        # Test train and save of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/train', 'post',
                                       {
                                           "immediate_mode": True,
                                           "threshold": 10.0,
                                           # "clsfr_algorithm": "naive_bayes",
                                           # "language_model_list": [
                                           #     {
                                           #         "lang_code": "eng",
                                           #         "lang_model": "glove6B50D_trimmed"
                                           #     }
                                           # ]
                                       },
                                       200,
                                       {
                                           "name": "user_act",
                                           'cm_labels': {'0': 'help_class', '1': 'menu_class', '2': 'quit_class',
                                                         '_nc': '_nc'}
                                       }))

        # Test delete of single training sample.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'delete',
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "help question"
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "help question"
                                           }
                                       ],
                                       treat_list_as_set=True))

        # Test delete of training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples_all', 'delete',
                                       {},
                                       200,
                                       [
                                           {'label': 'menu_class', 'text': 'menu main'},
                                           {'label': 'quit_class', 'text': 'quit exit'}
                                       ],
                                       treat_list_as_set=True))

        # Add training samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'post',
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "help question"
                                           },
                                           {
                                               "label": "menu_class",
                                               "text": "menu main"
                                           },
                                           {
                                               "label": "quit_class",
                                               "text": "quit exit"
                                           }
                                       ],
                                       200,
                                       [{'label': 'help_class', 'lang_code': '', 'text': 'help question'},
                                        {'label': 'menu_class', 'lang_code': '', 'text': 'menu main'},
                                        {'label': 'quit_class', 'lang_code': '', 'text': 'quit exit'}]
                                       ))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act', 'delete',
                                       {},
                                       200,
                                       {"name": "user_act"}))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers', 'post',
                                       {"name": "user_act",
                                        "load_from_store": True},
                                       200,
                                       {"name": "user_act"}))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act', 'get',
                                       {},
                                       200,
                                       {
                                           "desc": "Text classifier to classify user actions requests.",
                                           "name": "user_act",
                                           'cm_labels': {'0': 'help_class', '1': 'menu_class', '2': 'quit_class',
                                                         '_nc': '_nc'}
                                       }))

        # Test get training data.
        response = check_response_request(self.client,
                                          '/nlu/v2/text_classifiers/user_act/training_samples', 'get',
                                          {})
        self.assertTrue(check_response_test(response,
                                            200,
                                            [
                                                {
                                                    "label": "help_class",
                                                    "text": "help question"
                                                },
                                                {
                                                    "label": "menu_class",
                                                    "text": "menu main"
                                                },
                                                {
                                                    "label": "quit_class",
                                                    "text": "quit exit"
                                                }
                                            ],
                                            treat_list_as_set=True))

        sample_uuid = response.json[1]['uuid']

        # Test update of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'put',
                                       [{"uuid": sample_uuid, "label": "menu_class", "text": "main menu",
                                         "lang_code": "eng"}],
                                       200,
                                       [{'label': 'menu_class', 'lang_code': 'eng', 'text': 'main menu',
                                         'uuid': sample_uuid}],
                                       treat_list_as_set=True))

        # Test delete of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'delete',
                                       [{"uuid": sample_uuid}],
                                       200,
                                       [{'label': 'menu_class', 'uuid': sample_uuid}],
                                       treat_list_as_set=True))

        # Add training samples back (ignoring duplicates).
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/training_samples', 'post',
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "help question"
                                           },
                                           {
                                               "label": "menu_class",
                                               "text": "menu main"
                                           },
                                           {
                                               "label": "quit_class",
                                               "text": "quit exit"
                                           }
                                       ],
                                       200,
                                       [{'label': 'menu_class', 'lang_code': '', 'text': 'menu main'}]
                                       ))

        # Test get testing data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/testing_samples', 'get',
                                       {},
                                       200,
                                       [
                                           {
                                               "label": "help_class",
                                               "text": "please help me"
                                           },
                                           {
                                               "label": "menu_class",
                                               "text": "Take me to the menu"
                                           },
                                           {
                                               "label": "quit_class",
                                               "text": "please quit"
                                           }
                                       ],
                                       treat_list_as_set=True))

        ######
        # Test retrieve.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/retrieve',
                                       'post',
                                       {"text": "Please take me to the main menu.",
                                        "lang_code": "eng"},
                                       200,
                                       [
                                           {'label': 'menu_class', 'probability': 1.0},
                                           {'label': 'help_class', 'probability': 1.6035533574597333e-39},
                                           {'label': 'quit_class', 'probability': 1.0501947604694985e-39}
                                       ]))

        # Test the TSNE calculation - start the task.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/tsne',
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
                                       '/nlu/v2/text_classifiers/user_act/tsne',
                                       'get',
                                       {},
                                       200,
                                       [],
                                       treat_list_as_set=True))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        ntc_meta_info = wrapper_util.ntc_dict.get('user_act_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(ntc_meta_info is not None)
        if ntc_meta_info is not None:
            ntc_meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO which would cause a
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/retrieve',
                                       'post',
                                       {"text": "Please take me to the main menu.",
                                        "lang_code": "eng"},
                                       200,
                                       [
                                           {'label': 'menu_class', 'probability': 1.0},
                                           {'label': 'help_class', 'probability': 1.6035533574597333e-39},
                                           {'label': 'quit_class', 'probability': 1.0501947604694985e-39}
                                       ]))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/retrieve',
                                       'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act', 'delete',
                                       {},
                                       200,
                                       {"name": "user_act"}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/text_classifiers/user_act/retrieve',
                                       'post',
                                       {"text": "Was the SDK programmed in C++?"},
                                       400,
                                       {'error_detail': 'Named instance user_act not loaded!'}))

        print('time = ' + str(time.time() - start_time))
        print()
