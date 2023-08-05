#!/usr/bin/env python3

import os
import logging
import time

import connexion
# from connexion.resolver import RestyResolver

from typing import List, Optional, Dict  # noqa # pylint: disable=unused-import
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import __version__ as __sqlalchemy_version__
from flask_cors import CORS

from prometheus_client import start_http_server
from prometheus_client import Gauge

LOGGERS_TO_IGNORE = [
       "connexion.operations.swagger2",
       "swagger_spec_validator.ref_validators",
       "connexion.operation",
       "connexion.apis.abstract",
       "connexion.apis.flask_api",
       "connexion.app",
       "connexion.decorators.validation",
       "connexion.decorators.parameter",
       "werkzeug",
       "matplotlib"
]  # type: List[str]

db = SQLAlchemy()

_logging_details = {}  # type: Dict

_celery_available = False


def check_celery_available() -> bool:
    return _celery_available


def get_log_filename() -> Optional[str]:
    return _logging_details.get("filename")


def reset_logging():
    """ Remove the handlers and filters from the logger to prevent, for example,
    handlers stacking up over multiple runs."""
    root = logging.getLogger()

    for handler in list(root.handlers):  # list(...) makes a copy of the handlers list.
        root.removeHandler(handler)
        handler.close()

    for filter in list(root.filters):  # list(...) makes a copy of the handlers list.
        root.removeFilter(filter)


class PrometheusHandler(logging.Handler):
    """ Custom logging handler to send error events to Prometheus. Meant to be used at log level of error."""
    def __init__(self):
        logging.Handler.__init__(self)

        # Counter of number of emitted events.
        self.promths_emit_count_gauge = Gauge('feersum_nlu_logging_emit_count',
                                              'FeersumNLU - Number of logging errors emitted.',
                                              ['desc'])

    def emit(self, record):
        try:
            if record.levelno >= logging.CRITICAL:
                self.promths_emit_count_gauge.labels(desc='critical').inc()  # pylint: disable=no-member
            elif record.levelno >= logging.ERROR:
                self.promths_emit_count_gauge.labels(desc='error').inc()  # pylint: disable=no-member
            elif record.levelno >= logging.WARNING:
                self.promths_emit_count_gauge.labels(desc='warning').inc()  # pylint: disable=no-member
            elif record.levelno >= logging.INFO:
                self.promths_emit_count_gauge.labels(desc='info').inc()  # pylint: disable=no-member
            elif record.levelno >= logging.DEBUG:
                self.promths_emit_count_gauge.labels(desc='debug').inc()  # pylint: disable=no-member
        except Exception:
            raise


def setup_logging(requested_logging_path: str = "~/.nlu/logs",
                  include_prometheus: bool = False):
    """ Setup logging to file and stderr. """
    global _logging_details

    reset_logging()

    # Set all loggers to 'ignore' to show only ERROR level logs or higher.
    for LOGGER in LOGGERS_TO_IGNORE:
        logging.getLogger(LOGGER).setLevel("ERROR")

    logging_path = os.path.expanduser(requested_logging_path)
    # print("rest_flask_app.setup_logging : logging_path =", logging_path)

    # Create the logging path if it doesn't already exist.
    os.makedirs(logging_path, exist_ok=True)

    logger = logging.getLogger()  # Root logger.

    # Log Levels!:
    # CRITICAL 50
    # ERROR    40
    # WARNING  30
    # INFO     20
    # DEBUG    10
    # NOTSET    0

    logger.setLevel(logging.DEBUG)

    _logging_details["filename"] = "nlp_engine_" + str(time.strftime("%Y-%m-%d")) + "_" + \
                                   str(time.strftime("%Hh%Mm%Ss")) + ".log"
    print(_logging_details)

    # Create file handler.
    fh = logging.FileHandler(logging_path + "/" + _logging_details["filename"])
    fh.setLevel(logging.DEBUG)

    # Create console handler.
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers.
    formatter = logging.Formatter('%(asctime)s, %(name)s, %(levelname)s, %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to logger.
    logger.addHandler(ch)
    logger.addHandler(fh)

    if include_prometheus:
        # Create Prometheus handler - sends number of WARNINGS+ to prometheus!
        ph = PrometheusHandler()
        ph.setLevel(logging.WARNING)
        ph.setFormatter(formatter)
        logger.addHandler(ph)

    logging.info(f"rest_flask_utils.setup_logging: Logging started!")


def _setup_db(connexion_app: connexion.FlaskApp):
    """Setup and activate the DB within the Flask app."""
    db.init_app(connexion_app.app)
    connexion_app.app.app_context().push()  # Binds the app context to the current context.
    logging.info(f"rest_flask_utils._setup_db: sqlalchemy.__version__ = {__sqlalchemy_version__}.")


def _setup_api(connexion_app: connexion.FlaskApp, debug: bool, swagger_ui: bool):
    """Setup the rest API within the Flask app."""
    connexion_app.add_api(specification='swagger.yaml',
                          arguments={'title': 'This is the HTTP API for Feersum NLU. '
                                              'See https://github.com/praekelt/feersum-nlu-api-wrappers '
                                              'for examples of how to use the API.'},
                          options={"debug": debug, "swagger_ui": swagger_ui})


def _get_celery_worker_status(celery_app):
    i = celery_app.control.inspect()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }

    logging.info(f"rest_flask_utils._get_celery_worker_status: {result}.")

    return result


def create_celery_app(connexion_app: connexion.FlaskApp,
                      enable_background_training: bool,
                      main=None):
    """Setup the Celery app within the Flask app."""
    print("  Creating celery app...", flush=True)
    global _celery_available

    connexion_app.app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    # connexion_app.app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    # connexion_app.app.config['CELERY_RESULT_BACKEND'] = 'file:///var/celery/results'

    if not enable_background_training:
        connexion_app.app.config['CELERY_TASK_ALWAYS_EAGER'] = True

    print("  Celery(...)...", flush=True)
    if main is None:
        celery_app = Celery(connexion_app.app.name, broker=connexion_app.app.config['CELERY_BROKER_URL'])
    else:
        celery_app = Celery(main, broker=connexion_app.app.config['CELERY_BROKER_URL'])

    celery_app.conf.update(connexion_app.app.config)
    celery_app.conf.task_serializer = 'pickle'

    if enable_background_training:
        logging.debug("rest_flask_utils._setup_celery_app Running _get_celery_worker_status(...)...")
        logging.debug("rest_flask_utils._setup_celery_app     [Note: This might hang if broker not available!]")

        # print("  _get_celery_worker_status(...)...", flush=True)
        # print("     [Note: This might hang if broker not available!]")

        status = _get_celery_worker_status(celery_app)

        logging.debug("rest_flask_utils._setup_celery_app Running _get_celery_worker_status(...)... Done.")

        if status.get('stats') is None:
            _celery_available = False
            logging.error(f"rest_flask_utils._setup_celery_app - Celery requested, but NOT available!")
        else:
            logging.info(f"rest_flask_utils._setup_celery_app - Celery is available.")
            _celery_available = True
    else:
        _celery_available = False

    print(f" Background training = {_celery_available}")
    print("  Done (creating celery app).", flush=True)
    print()

    return celery_app


promths_idle_fraction_gauge = Gauge('feersum_nlu_flask_idle_fraction', 'FeersumNLU - Flask Idle Fraction')
last_operation_start_time = 0.0
last_operation_end_time = 0.0


def cllbck_before_flask_request():
    global last_operation_start_time
    global last_operation_end_time

    current_time = time.time()

    if last_operation_end_time != 0.0:
        idle_time = round(current_time - last_operation_end_time, 4)
        total_time = round(current_time - last_operation_start_time, 4)
        promths_idle_fraction_gauge.set(idle_time / total_time)

    last_operation_start_time = current_time


def cllbck_after_flask_request(response):
    global last_operation_end_time

    last_operation_end_time = time.time()
    return response


def create_flask_app(add_api: bool,
                     swagger_ui: bool,
                     database_url: str,
                     debug: bool):
    """
    Create the  Flask/Connexion app and the Flask-SQLAlchemy DB interface.
    The swagger spec is used to build an API if add_api == True!
    """
    print("Creating flask app...", flush=True)
    app = connexion.App(__name__, specification_dir='./rest_api/flask_server/swagger/',
                        debug=debug)

    app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Remove significant overhead from track modifications.
    app.app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    if debug:
        app.app.config['TESTING'] = True
        # app.app.config["SQLALCHEMY_ECHO"] = True

    print("  _setup_db...", flush=True)
    _setup_db(app)

    print("  _setup_api...", flush=True)
    if add_api:
        _setup_api(app, debug=debug, swagger_ui=swagger_ui)

    print("Done (creating flask app).", flush=True)
    print()

    app.app.before_request(cllbck_before_flask_request)
    app.app.after_request(cllbck_after_flask_request)

    # add CORS support
    CORS(app.app)

    return app


def create_prometheus_server(prometheus_port: int):
    print("Creating promethius server...", flush=True)
    logging.info(f"rest_flask_utils.create_prometheus_server: Creating promethius server.")
    start_http_server(prometheus_port)
    print("Done (creating promethius server).", flush=True)
    print()
