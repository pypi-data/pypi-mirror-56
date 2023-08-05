from __future__ import absolute_import, unicode_literals
import os
import sys

# from celery import Celery

from feersum_nlu.rest_flask_utils import create_flask_app
from feersum_nlu.rest_flask_utils import create_celery_app

from feersum_nlu.rest_flask_utils import setup_logging

from feersum_nlu.rest_api.wrapper_util import load_shared_models as wrapper_load_shared_models

from feersum_nlu.rest_api.wrapper_util import start_nlp_engine as wrapper_start_nlp_engine
from feersum_nlu.rest_api.wrapper_util import start_vision_engine as wrapper_start_vision_engine  # noqa

# Change working directory to match Flask configuration
# os.chdir("./feersum_nlu")

setup_logging()

# Get the production or local URL from the OS env variable.
database_url = os.environ.get("FEERSUM_NLU_DATABASE_URL")

if database_url is None:
    sys.exit("FEERSUM_NLU_DATABASE_URL env variable is not configured. See the 'local_db' make target to create a local "
             "test database for URL postgresql://127.0.0.1:5432/feersumnlu?user=feersumnlu&password=feersumnlu")

wrapper_start_nlp_engine(use_duckling=False)
wrapper_start_vision_engine()

# Create the flask app (without an API or UI) only to activate the db.
flask_app = create_flask_app(add_api=False, swagger_ui=False,
                             database_url=database_url,
                             debug=False)

celery_app = create_celery_app(flask_app,
                               enable_background_training=False,
                               main="project")

# Pre-load all the word embeddings and other shared models.
wrapper_load_shared_models(lm_name_list=[],
                           vm_name_list=[])

# Manually register tasks by importing modules
import feersum_nlu.rest_api.tasks  # noqa
