from typing import Optional
from feersum_nlu.rest_flask_utils import db


class WrapperBlobData(db.Model):
    """ The model's meta info that typically holds the wrapper level data like trashed flag, training data, etc. """
    __tablename__ = "wrapper_blob_data"

    # Model name key e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a.text_clsfr_meta_pickle
    name = db.Column(db.String(1024), primary_key=True)

    # Binary blob (i.e. pickle) of the model's meta info. Should perhaps use a json blob?
    blob = db.Column(db.LargeBinary, nullable=False)

    # Unique model uuid used for caching and revision control.
    uuid = db.Column(db.String, nullable=False)

    trashed = db.Column(db.Boolean, nullable=False)

    def __init__(self,
                 _name: str,
                 _blob,
                 _uuid: str,
                 _trashed: bool) -> None:
        self.name = _name
        self.blob = _blob
        self.uuid = _uuid
        self.trashed = _trashed


class WrapperBlobDataVersioned(db.Model):
    __tablename__ = "wrapper_blob_data_versioned"

    name = db.Column(db.String(1024), primary_key=True)
    version = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    blob = db.Column(db.LargeBinary, nullable=False)
    uuid = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=True)

    def __init__(self,
                 _name: str,
                 _blob,
                 _uuid: str,
                 _message: Optional[str]) -> None:
        self.name = _name
        self.blob = _blob
        self.uuid = _uuid
        self.message = _message


class SDKBlobData(db.Model):
    """ The SDK model' blob. """
    __tablename__ = "sdk_blob_data"

    # Model name key e.g. my_txt_clsfr_b8349672-4c9b-415f-a839-6cd45524167a.crf_extr_pickle
    name = db.Column(db.String(1024), primary_key=True)

    # Binary blob of the SDK model. Possibly a pickle.
    blob = db.Column(db.LargeBinary, nullable=False)

    # Unique model uuid used for caching. Note: Need not be the same as the model's meta-info uuid!
    uuid = db.Column(db.String, nullable=False)

    def __init__(self,
                 _name: str,
                 _blob,
                 _uuid: str) -> None:
        self.name = _name
        self.blob = _blob
        self.uuid = _uuid


class APIKeyData(db.Model):
    __tablename__ = "api_key_data"

    auth_key = db.Column(db.String(1024), primary_key=True)
    desc = db.Column(db.String(1024), primary_key=False)

    call_count = db.Column(db.Integer, primary_key=False)
    call_count_limit = db.Column(db.Integer, primary_key=False)

    def __init__(self,
                 _auth_key: str,
                 _desc: str,
                 _call_count: int,
                 _call_count_limit: Optional[int]) -> None:
        self.auth_key = _auth_key
        self.desc = _desc
        self.call_count = _call_count
        self.call_count_limit = _call_count_limit


class AdminAPIKeyData(db.Model):
    __tablename__ = "admin_api_key_data"

    auth_key = db.Column(db.String(1024), primary_key=True)
    desc = db.Column(db.String(1024), primary_key=False)

    def __init__(self,
                 _auth_key: str,
                 _desc: str) -> None:
        self.auth_key = _auth_key
        self.desc = _desc


class APICallCountBreakdownData(db.Model):
    __tablename__ = "api_callcount_breakdown_data"

    auth_key = db.Column(db.String(1024), primary_key=True)
    endpoint = db.Column(db.String, primary_key=True)
    call_count = db.Column(db.Integer, primary_key=False)

    def __init__(self,
                 _auth_key: str,
                 _endpoint: str,
                 _call_count: int) -> None:
        self.auth_key = _auth_key
        self.endpoint = _endpoint
        self.call_count = _call_count
