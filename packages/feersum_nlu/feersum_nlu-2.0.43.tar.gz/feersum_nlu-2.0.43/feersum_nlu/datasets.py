from feersum_nlu import nlp_engine_data
import pandas as pd


__all__ = ['IMDB_SMALL', 'IMDB']

BUCKET_CREDS = nlp_engine_data.get_path() + '/bucket_creds.json'

DATASETS_BUCKET = "io-feersum-vectors-nlu-prod"
DATASETS_FOLDER = 'feersum_datasets'

# MODELS_BUCKET = "io-feersum-vectors-nlu-prod"
# MODELS_FOLDER = ""

# Datasets
IMDB_SMALL = 'IMDB/imdb-small.csv'
IMDB = 'IMDB/imdb.csv'
AG_NEWS = ''
AMAZON_REVIEWS = ''


# Models
# ELMO = f'{MODELS_BUCKET}/{MODELS_FOLDER}/ELMo/elmo.pkl'


def load(file_name):
    """given  the name of a dataset in the feersum data repo import that dataset and load into a pandas Dataframe"""

    file_path, file_name = nlp_engine_data.get_blob_from_gcp_bucket(blob_folder_name=DATASETS_FOLDER,
                                                                    blob_file_name=file_name,
                                                                    bucket_name=DATASETS_BUCKET)

    print(f"datasets.load: Local dataset file is at {file_path}/{file_name}")

    fname = f"{file_path}/{file_name}"
    df = pd.read_csv(fname)
    return df


def list_datasets():
    return __all__

# # TODO : implement file uncompress
# def untar_data(self, name):
#     """ large datasets stored in compressed format need to be uncompressed before loading into csv"""
#
#     pass
#     return

# TODO : implement similar functionality for pretrained models
# class Models(object):
#     """
#         A class for downloading pretrained models stored on feersum's cloud platform - GCP Bucket.
#
#     """
#
#     def __init__(self, file_name):
#         self.file_name = file_name
#
#     ELMO = f''

# TODO: Have the functionality to list files available for DL and their relative sizes
# TODO: Add info about each dataset, original source, preprocessing done, size, columns, datatypes
