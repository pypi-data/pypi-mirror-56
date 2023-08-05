"""
FeersumNLU Service - Managing auth token.

"""

import os
import sys

# NOTE: The below import is useful to bring feersum_nlu into the Python path!
module_path = os.path.abspath(os.path.join('.'))
print("module_path =", module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

from feersum_nlu.rest_flask_utils import create_flask_app  # noqa
from feersum_nlu.rest_flask_utils import create_celery_app  # noqa

from feersum_nlu.rest_flask_utils import setup_logging  # noqa

from feersum_nlu import nlp_engine  # noqa
from feersum_nlu import nlp_engine_data  # noqa

from feersum_nlu.rest_api.wrapper_util import add_auth_token  # noqa
from feersum_nlu.rest_api.wrapper_util import remove_admin_auth_token  # noqa
from feersum_nlu.rest_api.wrapper_util import get_auth_token_details  # noqa
from feersum_nlu.rest_api.wrapper_util import load_auth_token_list  # noqa
from feersum_nlu.rest_api.wrapper_util import load_admin_auth_token_list  # noqa


# from feersum_nlu.rest_api.wrapper_util import start_wrapper_nlp_engine  # noqa


def main():
    setup_logging()

    # Get the production or local URL from the OS env variable.
    database_url = os.environ.get("FEERSUM_NLU_DATABASE_URL")

    if database_url is None:
        sys.exit("FEERSUM_NLU_DATABASE_URL env variable is not configured. See the 'local_db' make target to create a local "
                 "test database for URL postgresql://127.0.0.1:5432/feersumnlu?user=feersumnlu&password=feersumnlu")

    # start_NLPEngine(use_duckling=False)

    # Create the flask app (without an API or UI) only to activate the db.
    flask_app = create_flask_app(add_api=False,
                                 swagger_ui=False,
                                 database_url=database_url,
                                 debug=True)

    # celery_app = \
    create_celery_app(flask_app,
                      enable_background_training=False)

    print('[Feersum NLU version = ' + nlp_engine.get_version() + ']')
    print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']')
    print()

    print("Admin auth token list...")
    print(load_admin_auth_token_list())
    print()

    print("Auth token list...")
    print(load_auth_token_list())
    print()

    print("Removing & Adding auth tokens...")

    print(remove_admin_auth_token('f6e8286f-3fee-4e0d-b847-0ca1241d2c00'))

    # Add auth token with absolute call limit.
    add_auth_token('FEERSUM-NLU-431-9020-80dd-cec15695d7', "Test token", 5000)  # desc, free calls.
    print(get_auth_token_details('FEERSUM-NLU-431-9020-80dd-cec15695d7'))

    # Add auth token with call limit relative to current call count.
    add_auth_token('FEERSUM-NLU-431-9020-80dd-cec15695d7', "Test token", 5000, True)  # desc, free calls (relative).
    print(get_auth_token_details('FEERSUM-NLU-431-9020-80dd-cec15695d7'))

    print("done.")
    print()


if __name__ == '__main__':
    main()
