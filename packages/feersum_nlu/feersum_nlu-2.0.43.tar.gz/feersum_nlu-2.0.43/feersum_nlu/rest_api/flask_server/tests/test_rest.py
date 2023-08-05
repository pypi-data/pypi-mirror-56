# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRest(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, True,  # use_duckling = True
                              *args, **kwargs)

    def test_date_parser(self):
        print("Rest HTTP test_date_parser:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'get',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'put',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'delete',
                                       {},
                                       405,
                                       {}))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'post',
                                       {"text": "20 september 2017"},
                                       200,
                                       [
                                           {
                                               "value": "2017-09-20 00:00:00",
                                               "granularity": "day"
                                           }
                                       ]))

        # Test retrieve
        print("Test retrieve")
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'post',
                                       {"text": "The day after 20 september 2017 at 8 in the evening."},
                                       200,
                                       [
                                           {
                                               "value": "2017-09-21 20:00:00",
                                               "granularity": "hour"
                                           }
                                       ]))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'post',
                                       {"text": "Not really a date."},
                                       200,
                                       []))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/date_parsers/generic/retrieve', 'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        print('time = ' + str(time.time() - start_time))
        print()

    def test_sentiment_detector(self):
        print("Rest HTTP test_sentiment_detector:")
        start_time = time.time()

        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'get',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'put',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'delete',
                                       {},
                                       405,
                                       {}))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'post',
                                       {"text": "I am happy!"},
                                       200,
                                       {"value": 0.6114}))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'post',
                                       {"text": "I am sad!"},
                                       200,
                                       {"value": -0.5255}))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/sentiment_detectors/generic/retrieve', 'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        print('time = ' + str(time.time() - start_time))
        print()

    def test_emotion_classifier(self):
        print("Rest HTTP test_emotion_classifier:")
        start_time = time.time()

        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'get',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'put',
                                       {},
                                       405,
                                       {}))

        # Test 405 return on unsupported method.
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'delete',
                                       {},
                                       405,
                                       {}))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'post',
                                       {"text": "I am happy!"},
                                       200,
                                       [{'label': 'joy', 'probability': 0.9486347436904907}]))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'post',
                                       {"text": "I am sad!"},
                                       200,
                                       [{'label': 'sadness', 'probability': 1.0}]))

        # Test retrieve
        self.assertTrue(check_response(self.client,
                                       '/nlu/v2/emotion_classifiers/generic/retrieve', 'post',
                                       {},
                                       400,
                                       {"detail": "'text' is a required property"}))

        print('time = ' + str(time.time() - start_time))
        print()
