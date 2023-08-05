from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import os
import sys

# NOTE: The below import is useful to bring feersum_nlu into the Python path!
module_path = os.path.abspath(os.path.join('..'))
print("module_path =", module_path)
if module_path not in sys.path:
    sys.path.append(module_path)

from feersum_nlu.rest_flask_utils import db, create_flask_app  # noqa
from feersum_nlu.rest_flask_utils import create_celery_app  # noqa

from feersum_nlu.db_models import SDKBlobData  # noqa
from feersum_nlu.db_models import WrapperBlobData  # noqa
from feersum_nlu.db_models import APIKeyData  # noqa
from feersum_nlu.db_models import AdminAPIKeyData  # noqa
from feersum_nlu.db_models import APICallCountBreakdownData  # noqa

# Get the production or local DB URL from the OS env variable.
database_url = os.environ.get("FEERSUM_NLU_DATABASE_URL")

if database_url is None:
    sys.exit("FEERSUM_NLU_DATABASE_URL env variable is not configured. See the 'local_db' make target to create a local "
             "test database for URL postgresql://127.0.0.1:5432/feersumnlu?user=feersumnlu&password=feersumnlu")

# wrapper_util.start_NLPEngine()

# Create the flask app (without an API or UI) only to activate the db.
flask_app = create_flask_app(add_api=False, swagger_ui=False,
                             database_url=database_url,
                             debug=True)

celery_app = create_celery_app(flask_app,
                               enable_background_training=False)

migrate = Migrate(flask_app.app, db)
manager = Manager(flask_app.app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
