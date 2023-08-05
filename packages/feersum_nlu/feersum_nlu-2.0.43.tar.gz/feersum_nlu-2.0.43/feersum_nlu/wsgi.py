import os
import sys
import logging

# NOTE: The below import is useful to bring feersum_nlu into the Python path!
module_path = os.path.abspath(os.path.join('..'))
print("module_path =", module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

from feersum_nlu.rest_flask_app import create_flask_app  # noqa
from feersum_nlu.rest_flask_utils import create_celery_app  # noqa

from feersum_nlu.rest_flask_app import setup_logging  # noqa

from feersum_nlu.rest_flask_utils import create_prometheus_server  # noqa

from feersum_nlu.rest_api import wrapper_util  # noqa

from feersum_nlu.nlp_engine import feers_sent_encoder_prod_list as nlpe_feers_sent_encoder_prod_list  # noqa
from feersum_nlu.vision_engine import feers_img_encoder_prod_list as nlpe_feers_img_encoder_prod_list  # noqa


create_prometheus_server(9101)  # Port used in deployments.

setup_logging(include_prometheus=True)

# Get the production or local URL from the OS env variable.
database_url = os.environ.get("FEERSUM_NLU_DATABASE_URL")

if database_url is None:
    sys.exit("FEERSUM_NLU_DATABASE_URL env variable is not configured. See the 'local_db' make target to create a local "
             "test database for URL postgresql://127.0.0.1:5432/feersumnlu?user=feersumnlu&password=feersumnlu")

duckling_url = os.environ.get("FEERSUM_NLU_DUCKLING_URL")

if duckling_url is None:
    sys.exit("FEERSUM_NLU_DUCKLING_URL env variable is not configured. The duckling prod instance's url should be "
             "https://qonda.feersum.io.")

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
                             swagger_ui=True,
                             database_url=database_url,
                             debug=False)

# celery_app
celery_app = create_celery_app(flask_app,
                               enable_background_training=False)
application = flask_app.app

# Pre-load the language models that will likely be used.
wrapper_util.load_shared_models(lm_name_list=nlpe_feers_sent_encoder_prod_list,
                                vm_name_list=nlpe_feers_img_encoder_prod_list)

logging.info(f"wsgi.py: __name__ == {__name__}")

if __name__ == "__main__":
    logging.info(f"wsgi.py: __main__ Starting Flask app in Python __main__ .")
    flask_app.run()
