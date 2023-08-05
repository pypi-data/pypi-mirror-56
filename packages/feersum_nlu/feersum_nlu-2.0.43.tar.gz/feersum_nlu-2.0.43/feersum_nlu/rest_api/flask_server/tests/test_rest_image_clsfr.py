# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response, check_response_test, check_response_request
from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import nlp_engine_data

from feersum_nlu.image_utils import get_image_samples


# @unittest.skip("skipping during dev")
class TestRestImageClassifier(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,
                              *args, **kwargs)

    def test_image_classifier(self):
        print("Rest HTTP test_image_classifier:")
        start_time = time.time()

        model_name = "test_image_clsfr"

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test get detail when model not loaded.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}', 'get',
                                       {},
                                       400,
                                       {'error_detail': f'Named instance {model_name} not loaded!'}))

        # Test create.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/image_classifiers', 'post',
                                       {"name": model_name,
                                        "desc": "Image classifier to classify user actions requests.",
                                        "load_from_store": False},
                                       200,
                                       {"name": model_name}))

        train_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/train"
        test_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/test"

        training_list = get_image_samples(train_data_path, "cat")
        training_list.extend(get_image_samples(train_data_path, "dog"))

        testing_list = get_image_samples(test_data_path, "cat")
        testing_list.extend(get_image_samples(test_data_path, "dog"))

        training_list_json = [{"label": label, "image": image} for image, label in training_list]
        testing_list_json = [{"label": label, "image": image} for image, label in testing_list]

        # Add some training samples.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/training_samples', 'post',
                                       training_list_json,
                                       200,
                                       training_list_json))

        # Add some testing samples.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/testing_samples', 'post',
                                       testing_list_json,
                                       200,
                                       testing_list_json))

        #####
        # Test retrieve when not yet trained.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/retrieve',
                                       'post',
                                       {"image": testing_list_json[0]['image']},
                                       200,
                                       []))

        # Test train and save of model.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/train', 'post',
                                       {
                                           "immediate_mode": True,
                                           "threshold": 10.0,
                                           "clsfr_algorithm": "resnet152",
                                           "num_epochs": 15
                                       },
                                       200,
                                       {
                                           "name": model_name,
                                           'cm_labels': {'0': 'cat', '1': 'dog', '_nc': '_nc'}
                                       }))

        # Test delete of training samples.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/training_samples_all', 'delete',
                                       {},
                                       200,
                                       training_list_json,
                                       treat_list_as_set=True))

        # Add training samples back.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/training_samples', 'post',
                                       training_list_json,
                                       200,
                                       training_list_json))

        # Test trashing of model.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}', 'delete',
                                       {},
                                       200,
                                       {"name": model_name}))

        # Test restore/un-trash i.e. create from store.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/image_classifiers', 'post',
                                       {"name": model_name,
                                        "load_from_store": True},
                                       200,
                                       {"name": model_name}))

        # Test get detail.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}', 'get',
                                       {},
                                       200,
                                       {
                                           "desc": "Image classifier to classify user actions requests.",
                                           "name": model_name,
                                           'cm_labels': {'0': 'cat', '1': 'dog', '_nc': '_nc'}
                                       }))

        # Test get training data.
        response = check_response_request(self.client,
                                          f'/nlu/v2/image_classifiers/{model_name}/training_samples', 'get',
                                          {})
        self.assertTrue(check_response_test(response,
                                            200,
                                            training_list_json,
                                            treat_list_as_set=True))

        uuid_to_delete = response.json[3]['uuid']
        sample_json = response.json[3]

        # 5 - Test delete of a training sample using its uuid.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/training_samples', 'delete',
                                       [{"uuid": uuid_to_delete}],
                                       200,
                                       [{'label': 'cat', 'uuid': uuid_to_delete}],
                                       treat_list_as_set=True))

        # 6 - Add training samples back (ignoring duplicates).
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/training_samples', 'post',
                                       training_list_json,
                                       200,
                                       [{
                                           'label': 'cat',
                                           'image': sample_json['image']
                                       }]))

        # Test get testing data.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/testing_samples', 'get',
                                       {},
                                       200,
                                       testing_list_json,
                                       treat_list_as_set=True))

        ######
        # Test retrieve.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/retrieve',
                                       'post',
                                       {"image": testing_list_json[0]['image']},
                                       200,
                                       [
                                           {'label': 'cat'},
                                           {'label': 'dog'}
                                       ]))

        # Simulate the DB's meta info (JUST THE META INFO) updating by modifying local cache's uuid!
        meta_info = wrapper_util.image_classifier_dict.get(model_name + '_FEERSUM-NLU-591-4ba0-8905-996076e94d')
        self.assertTrue(meta_info is not None)
        if meta_info is not None:
            meta_info.uuid = '0000000-000-591-4ba0-8905-996076e94d'  # Some fake uuid

        # Test retrieve after updating JUST THE META INFO which would cause a
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/retrieve',
                                       'post',
                                       {"image": testing_list_json[0]['image']},
                                       200,
                                       [
                                           {'label': 'cat'},
                                           {'label': 'dog'}
                                       ]))

        # Test retrieve with no image.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/retrieve',
                                       'post',
                                       {},
                                       400,
                                       {'error_detail': 'No image provided!'}))

        # Test delete
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}', 'delete',
                                       {},
                                       200,
                                       {"name": model_name}))

        # Test retrieve when trashed.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_classifiers/{model_name}/retrieve',
                                       'post',
                                       {"image": testing_list_json[0]['image']},
                                       400,
                                       {'error_detail': f'Named instance {model_name} not loaded!'}))

        print('time = ' + str(time.time() - start_time))
        print()
