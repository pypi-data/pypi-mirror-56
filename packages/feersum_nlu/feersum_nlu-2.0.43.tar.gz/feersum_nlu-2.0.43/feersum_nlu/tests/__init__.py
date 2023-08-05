"""Unit test base class for Feersum NLP Engine Python Module."""
import unittest

from feersum_nlu.rest_flask_utils import create_flask_app, db
from feersum_nlu.rest_flask_utils import create_celery_app

from feersum_nlu.rest_flask_utils import setup_logging, reset_logging


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        setup_logging()

        # Local DB for testing - See 'local_db' make target.
        database_url = "postgresql://127.0.0.1:5432/test_feersumnlu?user=feersumnlu&password=feersumnlu"

        # Create the flask app to activate the db for all unit tests.
        flask_app = create_flask_app(add_api=False, swagger_ui=False,
                                     database_url=database_url,
                                     debug=True)

        # celery_app = \
        create_celery_app(flask_app,
                          enable_background_training=False)

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        reset_logging()
