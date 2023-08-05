# import unittest
import time

from feersum_nlu.rest_api.flask_server.tests import BaseTestCase, check_response
from feersum_nlu.rest_api import wrapper_util


# @unittest.skip("skipping during dev")
class TestRestHealthEndpoint(BaseTestCase):
    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, False,  # use_duckling = False
                              *args, **kwargs)

    def test_health_endpoint(self):
        print("Rest HTTP test_health_endpoint:")
        start_time = time.time()

        # Add the auth token used for testing.
        wrapper_util.add_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")
        wrapper_util.add_admin_auth_token("FEERSUM-NLU-591-4ba0-8905-996076e94d", "Test token")

        dashboard_check = check_response(self.client, "/nlu/v2/health", "get",
                                         {},
                                         200,
                                         {},
                                         treat_list_as_set=True)

        self.assertTrue(dashboard_check)

        print('time = ' + str(time.time() - start_time))
