# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util
from feersum_nlu import nlp_engine_data

from feersum_nlu.image_utils import load_image


# @unittest.skip("skipping during dev")
class TestRestImageReader(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,
                              *args, **kwargs)

    def test_image_reader(self):
        print("Rest HTTP test_image_reader:")
        start_time = time.time()

        model_name = "generic"

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        image_str = load_image(nlp_engine_data.get_path() + "/vision/disc5.jpg", ignore_resolution=True)
        print(f"Image is {len(image_str)/1024} kB")

        ######
        # Test retrieve.
        self.assertTrue(check_response(self.client,
                                       f'/nlu/v2/image_readers/{model_name}/retrieve',
                                       'post',
                                       {"image": image_str},
                                       200,
                                       []))

        print('time = ' + str(time.time() - start_time))
        print()
