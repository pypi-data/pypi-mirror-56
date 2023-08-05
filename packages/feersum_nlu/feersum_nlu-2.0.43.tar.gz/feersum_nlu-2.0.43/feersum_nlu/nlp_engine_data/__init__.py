"""The module of data included with Feersum NLP Engine."""

from typing import Tuple, Optional, List, Dict, Set
from google.cloud import storage
from itertools import islice
import logging
import csv
import os
import ntpath

from feersum_nlu import nlp_engine_data


def get_path() -> str:
    """Get the file path to the data module."""
    return getattr(nlp_engine_data, '__path__')[0]


def get_blob_from_gcp_bucket(blob_folder_name: str,
                             blob_file_name: str,
                             bucket_name: str = "io-feersum-vectors-nlu-prod") -> Tuple[str, str]:
    """ Download and cache a file from a GCP bucket.

    Download and cache a file from a GCP bucket. The bucket name local file cache path and bucket creds are pre-
    defined.

    :param blob_folder_name: The name of the GCP folder.
    :param blob_file_name: The name of the blob in blob_folder_name to get. Can be a path relative to blob_folder_name.
    :param bucket_name: The name of the GCP bucket .
    :return: The path to the locally cached file.
    """
    # See https://console.cloud.google.com/storage/browser/io-feersum-vectors-nlu-prod for one of the buckets.

    try:
        storage_client = storage.Client.from_service_account_json(get_path() + '/bucket_creds.json')

        # local_file_cache_path = get_path()
        local_cache_path = "/tmp/feersum_nlu"

        full_blob_file_name = f"{blob_folder_name}/{blob_file_name}"
        full_local_file_name = f"{local_cache_path}/{full_blob_file_name}"

        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob(full_blob_file_name)

        if blob is None:
            logging.error("get_blob_from_gcp_bucket - bucket or blob not found?")
            return "", full_blob_file_name

        blob_md5 = blob.md5_hash

        # Load MD5 file from cache.
        try:
            with open(f"{full_local_file_name}.md5", "r") as f:
                cached_blob_md5 = f.readline()  # type: Optional[str]
        except IOError:
            cached_blob_md5 = None

        if (cached_blob_md5 is None) or (blob_md5 != cached_blob_md5):
            # The local cache doesn't have the blob or has an outdated version.
            logging.info(f"get_blob_from_gcp_bucket - You don't have {full_blob_file_name} or "
                         f"cache outdated. Downloading ...")

            # Create the local cache folder if it doesn't exists.
            full_local_file_folder, _ = ntpath.split(full_local_file_name)
            if not os.path.exists(full_local_file_folder):
                os.makedirs(full_local_file_folder)

            blob.download_to_filename(full_local_file_name)

            logging.info(f"get_blob_from_gcp_bucket - Done downloading {blob_folder_name}/{blob_file_name}.")

            # Write MD5 file to cache.
            try:
                with open(f"{full_local_file_name}.md5", "w") as f:
                    f.write(blob_md5)
            except IOError:
                pass

        return local_cache_path, full_blob_file_name
    except FileNotFoundError:
        logging.error("get_blob_from_gcp_bucket - bucket credits not found?")
        return "", blob_file_name


def load_quora_data(questions_file_name: str,
                    training_ratio: int, testing_ratio: int,
                    min_group_size: int) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    """ Loads the question data (in quora format) and prepares training and testing sets of questions.

    :param questions_file_name: The quora format questions file.
    :param training_ratio: The number of training questions to use per answer.
    :param testing_ratio: The number of training questions to use per answer.
    :param min_group_size: The minimum sized question groups to use. Set to max training_ratio+testing_ratio to
    consistently have the same training and testing groups.
    """
    question_dict = {}  # type: Dict[int, Tuple[str, int]]  # qid, (qtext, gid)
    group_dict = {}  # type: Dict[int, Set[int]]  # set of question IDs per gid

    with open(questions_file_name, newline='') as csvfile:
        new_gid = 0

        csvdoc = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for row in islice(csvdoc, 1, None):
            try:
                q1_id = int(row[1])
                q2_id = int(row[2])

                q1_text = row[3]
                q2_text = row[4]

                is_same_question = row[5] == "1"

                q1_gid = -1
                q2_gid = -1

                if question_dict.get(q1_id) is not None:
                    q1_gid = question_dict[q1_id][1]

                if question_dict.get(q2_id) is not None:
                    q2_gid = question_dict[q2_id][1]

                # Update with a connected component analysis.
                # 1) Update question group IDs and merge groups if required.
                if is_same_question:
                    if q1_gid == -1 and q2_gid == -1:  # two unseen questions
                        q1_gid = new_gid
                        q2_gid = new_gid
                        new_gid += 1
                    elif q1_gid == -1:  # one unseen question q1
                        q1_gid = q2_gid
                    elif q2_gid == -1:  # one unseen question q2
                        q2_gid = q1_gid
                    else:  # both questions already assigned to groups so merge the two groups.
                        if q1_gid != q2_gid:
                            group_dict[q1_gid].update(group_dict[q2_gid])

                            # change all questions that was in second group to first group.
                            for q_id in group_dict[q2_gid]:
                                text, _ = question_dict[q_id]
                                question_dict[q_id] = (text, q1_gid)

                            group_dict.pop(q2_gid)  # key q2_gid is expected to be in dict.
                            q2_gid = q1_gid
                else:
                    if q1_gid == -1:  # unseen question
                        q1_gid = new_gid
                        new_gid += 1
                    if q2_gid == -1:  # unseen question
                        q2_gid = new_gid
                        new_gid += 1

                # 2) Add/re-add questions to question dict and update group_dict.
                question_dict[q1_id] = (q1_text, q1_gid)
                question_dict[q2_id] = (q2_text, q2_gid)

                if group_dict.get(q1_gid) is None:
                    group_dict[q1_gid] = set()  # Set[int]

                if group_dict.get(q2_gid) is None:
                    group_dict[q2_gid] = set()  # Set[int]

                group_dict[q1_gid].add(q1_id)
                group_dict[q2_gid].add(q2_id)

            except (IndexError, ValueError) as e:
                print(e, row)
                return [], []

    training_list = []  # type: List[Tuple[str, str, str]]
    testing_list = []  # type: List[Tuple[str, str, str]]

    for _, question_set in group_dict.items():
        if len(question_set) >= min_group_size:
            for qid in islice(question_set, 0, training_ratio):
                text, gid = question_dict[qid]
                training_list.append((text, str(gid), 'eng'))

            for qid in islice(question_set, training_ratio, training_ratio + testing_ratio):
                text, gid = question_dict[qid]
                testing_list.append((text, str(gid), 'eng'))

    return training_list, testing_list
