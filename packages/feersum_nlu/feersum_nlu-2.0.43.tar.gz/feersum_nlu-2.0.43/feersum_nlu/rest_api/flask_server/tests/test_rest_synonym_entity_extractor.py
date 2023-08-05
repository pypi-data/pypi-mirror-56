# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_request, check_response_test
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestSynonymEntityExtractor(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_synonym_entity_extractor(self):
        print("Rest HTTP test_synonym_entity_extractor:", flush=True)
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1', 'get',
                                       {},
                                       400,
                                       {'error_detail': 'Named instance synonym1 not loaded!'}))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors', 'post',
                                       {"name": "synonym1",
                                        "desc": "Synonym extractor for the Feersum NLU SDK.",
                                        "load_from_store": False},
                                       200,
                                       {"name": "synonym1"}))

        # Add some training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/training_samples',
                                       'post',
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food",
                                                        "ignore_case": True, "ignore_word_boundaries": True},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer'],
                                                        "ignore_case": True, "ignore_word_boundaries": False}
                                                   ]
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 6},
                                                   {'entity': 'food', 'index': 25, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a burger with chips please?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 22, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a slice of pizza?'},
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 7}],
                                               'intent': None,
                                               'text': 'Can I have a hot dog with mustard?'},
                                           {
                                               'entity_list': [
                                                   {'entity': 'food',
                                                    'syn_set': ['hamburger', 'fish', 'sandwich', 'beef']},
                                                   {'entity': 'drink',
                                                    'syn_set': ['water', 'wine', 'beer']}],
                                               'intent': None,
                                               'text': None
                                           }
                                       ]))

        # Add some testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/testing_samples', 'post',
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 6},
                                                   {'entity': 'food', 'index': 25, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a burger with chips please?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food',  'index': 22, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a slice of pizza?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 7}],
                                               'intent': None,
                                               'text': 'Can I have a hot dog with mustard?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food',
                                                    'syn_set': ['hamburger', 'fish', 'sandwich', 'beef']},
                                                   {'entity': 'drink',
                                                    'syn_set': ['water', 'wine', 'beer']}],
                                               'intent': None,
                                               'text': None
                                           }
                                       ]))
        #####
        # Test retrieve when not yet trained.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/retrieve',
                                       'post',
                                       {"text": "Was the SDK programmed in C++?"},
                                       200,
                                       []))

        # Test train and save of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/train',
                                       'post',
                                       {
                                           "threshold": 0.98,
                                       },
                                       200,
                                       {"name": "synonym1"}))

        # Test delete of training samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/training_samples_all', 'delete',
                                       {},
                                       200,
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       ))

        print("Test delete of single testing sample...", flush=True)

        # Test delete of single testing sample.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/testing_samples',
                                       'delete',
                                       [
                                           {
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                       ],
                                       200,
                                       [
                                           {
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                       ],
                                       ))

        # Test delete of testing samples.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/testing_samples_all', 'delete',
                                       {},
                                       200,
                                       [
                                           {
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       treat_list_as_set=True))

        # Add training samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/training_samples',
                                       'post',
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 6},
                                                   {'entity': 'food', 'index': 25, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a burger with chips please?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 22, 'len': 5}],
                                               'intent': None,
                                               'text': 'Can I have a slice of pizza?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 7}],
                                               'intent': None,
                                               'text': 'Can I have a hot dog with mustard?'
                                           },
                                           {
                                               'entity_list': [
                                                   {'entity': 'food',
                                                    'syn_set': ['hamburger', 'fish', 'sandwich', 'beef']},
                                                   {'entity': 'drink',
                                                    'syn_set': ['water', 'wine', 'beer']}],
                                               'intent': None,
                                               'text': None
                                           }
                                       ]))

        # Test get training data.
        response = check_response_request(self.client,
                                          f'/nlu/v2/synonym_entity_extractors/synonym1/training_samples', 'get',
                                          {})
        self.assertTrue(check_response_test(response,
                                            200,
                                            [],  # Don't care about return here.
                                            treat_list_as_set=True))

        uuid_to_delete = response.json[2]['uuid']

        # Test delete of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/synonym_entity_extractors/synonym1/training_samples', 'delete',
                                       [{"uuid": uuid_to_delete}],
                                       200,
                                       [{'text': 'Can I have a hot dog with mustard?', 'uuid': uuid_to_delete}],
                                       treat_list_as_set=True))

        # Add training samples back (ignoring duplicates).
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/synonym_entity_extractors/synonym1/training_samples', 'post',
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               'entity_list': [
                                                   {'entity': 'food', 'index': 13, 'len': 7}],
                                               'intent': None,
                                               'text': 'Can I have a hot dog with mustard?'
                                           }
                                       ]))

        # Add testing samples back.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/testing_samples', 'post',
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       200,
                                       [
                                           {
                                               'entity_list':
                                                   [
                                                       {'entity': 'food', 'index': 13, 'len': 6},
                                                       {'entity': 'food', 'index': 25, 'len': 5}
                                                   ],
                                               'intent': None,
                                               'text': 'Can I have a burger with chips please?'
                                           },
                                           {
                                               'entity_list':
                                                   [
                                                       {'entity': 'food', 'index': 22, 'len': 5}
                                                   ],
                                               'intent': None,
                                               'text': 'Can I have a slice of pizza?'},
                                           {
                                               'entity_list':
                                                   [
                                                       {'entity': 'food', 'index': 13, 'len': 7}
                                                   ],
                                               'intent': None,
                                               'text': 'Can I have a hot dog with mustard?'
                                           },
                                           {
                                               'entity_list':
                                                   [
                                                       {'entity': 'food', 'syn_set': ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {'entity': 'drink', 'syn_set': ['water', 'wine', 'beer']}
                                                   ],
                                               'intent': None,
                                               'text': None
                                           }
                                       ]))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1', 'delete',
                                       {},
                                       200,
                                       {"name": "synonym1"}))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors', 'post',
                                       {"name": "synonym1",
                                        "load_from_store": True},
                                       200,
                                       {"name": "synonym1"}))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1', 'get',
                                       {},
                                       200,
                                       {
                                           "desc": "Synonym extractor for the Feersum NLU SDK.",
                                           "name": "synonym1"
                                       }))

        # Test get training data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/training_samples',
                                       'get',
                                       {},
                                       200,
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                           },
                                           {  # Example of training sample with only synsets!
                                           }
                                       ], treat_list_as_set=True
                                       ))

        # Test get testing data.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/testing_samples',
                                       'get',
                                       {},
                                       200,
                                       [
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a burger with chips please?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 6, "entity": "food"},
                                                       {"index": 25, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a slice of pizza?",
                                               "entity_list":
                                                   [
                                                       {"index": 22, "len": 5, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with text and some entities.
                                               "text": "Can I have a hot dog with mustard?",
                                               "entity_list":
                                                   [
                                                       {"index": 13, "len": 7, "entity": "food"}
                                                   ]
                                           },
                                           {  # Example of training sample with only synsets!
                                               "entity_list":
                                                   [
                                                       {"entity": "food", "syn_set": ['hamburger', 'fish',
                                                                                      'sandwich', 'beef']},
                                                       {"entity": "drink", "syn_set": ['water', 'wine', 'beer']}
                                                   ]
                                           }
                                       ],
                                       ))

        ######
        # Test retrieve.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/retrieve',
                                       'post',
                                       {"text": "I would like to buy Beef Sandwiches with mustard."},
                                       200,
                                       [
                                           {"index": 20, "len": 4, "entity": "food"},
                                           {"index": 25, "len": 8, "entity": "food"}
                                       ],
                                       treat_list_as_set=True))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        synonym_meta_info = wrapper_util.synonym_extr_dict.get('synonym1_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(synonym_meta_info is not None)
        if synonym_meta_info is not None:
            synonym_meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # entity_wrapper_synonym.synonym_extr_trash_helper('synonym1_FEERSUM-NLU-591-4ba0-8905-996076e94d')

        # Test retrieve after updating JUST THE META INFO.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/retrieve',
                                       'post',
                                       {"text": "I would like to buy Beef Sandwiches with mustard."},
                                       200,
                                       [
                                           {"index": 20, "len": 4, "entity": "food"},
                                           {"index": 25, "len": 8, "entity": "food"}
                                       ],
                                       treat_list_as_set=True))

        # Test retrieve with no text.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/retrieve',
                                       'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1', 'delete',
                                       {},
                                       200,
                                       {"name": "synonym1"}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/synonym_entity_extractors/synonym1/retrieve',
                                       'post',
                                       {"text": "I would like to buy a beef sandwich with mustard."},
                                       400,
                                       {'error_detail': 'Named instance synonym1 not loaded!'}))

        print('time = ' + str(time.time() - start_time))
        print()
