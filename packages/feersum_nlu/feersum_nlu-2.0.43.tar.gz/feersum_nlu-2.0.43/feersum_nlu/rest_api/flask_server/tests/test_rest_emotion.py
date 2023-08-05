# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestEmotion(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_emotion(self):
        print("Rest HTTP test_emotion:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'post',
                                       {
                                           "text": "BIG thank you for liking my little Pumpkin  :)  She's the smallest of "
                                                   "my 4, but is very playful &amp; wakes me up most mornings."
                                       },
                                       200,
                                       [{'label': 'joy', 'probability': 0.999822199344635}]
                                       ))

        print('time = ' + str(time.time() - start_time))
        print()
