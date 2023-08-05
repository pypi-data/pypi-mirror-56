# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestSentiment(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_sentiment(self):
        print("Rest HTTP test_sentiment:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        ######
        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'post',
                                       {
                                           "text": "This is a great example of a good positive sentiment 👍."
                                       },
                                       200,
                                       {'detail_list': [{'index': 0, 'len': 55, 'value': 1.0}], 'value': 1.0}
                                       ))

        print('time = ' + str(time.time() - start_time))
        print()
