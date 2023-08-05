#!/usr/bin/env python3

import os
import sys
import logging
import argparse

# NOTE: The below import is useful to bring feersum_nlu into the Python path!
module_path = os.path.abspath(os.path.join('..'))
print("module_path =", module_path, flush=True)

if module_path not in sys.path:
    sys.path.append(module_path)

from feersum_nlu.rest_flask_utils import create_flask_app  # noqa
from feersum_nlu.rest_flask_utils import create_celery_app  # noqa

from feersum_nlu.rest_flask_utils import setup_logging  # noqa
from feersum_nlu.rest_flask_utils import create_prometheus_server  # noqa

from feersum_nlu.rest_api import wrapper_util  # noqa

# from feersum_nlu.nlp_engine import feers_sent_encoder_prod_list as nlpe_feers_sent_encoder_prod_list  # noqa
# from feersum_nlu.vision_engine import feers_img_encoder_prod_list as nlpe_feers_img_encoder_prod_list  # noqa


def main():
    server_port = 8100  # Default server port.
    swagger_ui = True
    enable_background_training = False

    ap = argparse.ArgumentParser()
    ap.add_argument("--server_port", required=True, type=int,
                    help=f"The server port. Default is --server_port={server_port}")
    ap.add_argument("--enable_background_training", action="store_true",
                    help=f"Use background training if specified.")

    args = vars(ap.parse_args())
    server_port = args.get('server_port', server_port)
    enable_background_training = args.get('enable_background_training', enable_background_training)

    print('Arguments =', args)
    print('server_port =', server_port)
    print('enable_background_training =', enable_background_training)

    prometheus_port = server_port + 1500  # Server ports are like 9600, 9601, 9602
    print('prometheus_port =', prometheus_port)
    create_prometheus_server(prometheus_port)

    # Get the logging path from the OS env variable.
    logging_path = os.environ.get("FEERSUM_NLU_LOGGING_PATH", "~/.nlu/logs")
    setup_logging(requested_logging_path=logging_path,
                  include_prometheus=True)

    # Get the production or local URL from the OS env variable.
    database_url = os.environ.get("FEERSUM_NLU_DATABASE_URL")

    if database_url is None:
        sys.exit("FEERSUM_NLU_DATABASE_URL env variable is not configured. See the 'local_db' make target to create a local "
                 "test database for URL postgresql://127.0.0.1:5432/feersumnlu?user=feersumnlu&password=feersumnlu")
    print("database_url =", database_url)

    duckling_url = os.environ.get("FEERSUM_NLU_DUCKLING_URL")

    if duckling_url is None:
        sys.exit("FEERSUM_NLU_DUCKLING_URL env variable is not configured. The duckling prod instance's url should be "
                 "https://qonda.feersum.io.")
    print("duckling_url =", duckling_url)

    wrapper_util.intent_retrieve_MAX_TEXT_LENGTH = int(os.environ.get("FEERSUM_NLU_INTENT_RETRIEVE_MAX_TEXT_LENGTH",
                                                                      wrapper_util.intent_retrieve_MAX_TEXT_LENGTH))

    wrapper_util.faq_retrieve_MAX_TEXT_LENGTH = int(os.environ.get("FEERSUM_NLU_FAQ_RETRIEVE_MAX_TEXT_LENGTH",
                                                                   wrapper_util.faq_retrieve_MAX_TEXT_LENGTH))

    wrapper_util.entity_retrieve_MAX_TEXT_LENGTH = int(os.environ.get("FEERSUM_NLU_ENTITY_RETRIEVE_MAX_TEXT_LENGTH",
                                                                      wrapper_util.entity_retrieve_MAX_TEXT_LENGTH))

    print()
    print("FEERSUM_NLU_DATABASE_URL", database_url)
    print("FEERSUM_NLU_INTENT_RETRIEVE_MAX_TEXT_LENGTH", wrapper_util.intent_retrieve_MAX_TEXT_LENGTH)
    print("FEERSUM_NLU_FAQ_RETRIEVE_MAX_TEXT_LENGTH", wrapper_util.faq_retrieve_MAX_TEXT_LENGTH)
    print("FEERSUM_NLU_ENTITY_RETRIEVE_MAX_TEXT_LENGTH", wrapper_util.entity_retrieve_MAX_TEXT_LENGTH)
    print()

    wrapper_util.start_nlp_engine()
    wrapper_util.get_nlpe_engine().set_duckling_url(duckling_url)

    wrapper_util.start_vision_engine()

    flask_app = create_flask_app(add_api=True,
                                 swagger_ui=swagger_ui,
                                 database_url=database_url,
                                 debug=False)

    # celery_app
    create_celery_app(flask_app,
                      enable_background_training=enable_background_training)

    # Pre-load the language models that will likely be used.
    wrapper_util.load_shared_models(lm_name_list=[],
                                    vm_name_list=[])
    # wrapper_util.load_shared_models(lm_name_list=nlpe_feers_sent_encoder_prod_list,
    #                                 vm_name_list=nlpe_feers_img_encoder_prod_list)

    logging.info(f"rest_flask_app.py: Starting Flask app.")
    flask_app.run(server_port)


# run notes: python3 rest_flask_app.py
# Browse to http://localhost:8000/nlu/v2/ui/#/ to see the API.

if __name__ == '__main__':
    main()
