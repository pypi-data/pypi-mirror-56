from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import load_only

from typing import Dict, Tuple, List, Optional, Set, Any  # noqa # pylint: disable=unused-import

import io
import pickle

import sklearn
import sklearn.metrics
import logging
import uuid

import csv
from itertools import islice
import string

from feersum_nlu import __pickle_protocol_version__ as feersum_nlu_pickle_protocol_version
from feersum_nlu.db_models import SDKBlobData

from feersum_nlu import nlp_engine_data
from feersum_nlu.rest_flask_utils import db


# =========================================================================
# === Result Analysis =====================================================
# =========================================================================
def smplfy_confusion_matrix(confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]) -> \
        Dict[str, Dict[str, int]]:
    """
    Create a conf matrix with only cell counts not the actual samples behind the cells.

    :param confusion_dict: Full confusion dict with samples stored in matrix cells.
    :return: The simplified confusion dict with only sample count stored in matrix cells.
    """
    smpl_conf_dict = {}  # type: Dict[str, Dict[str, int]]

    for row_label, row_dict in confusion_dict.items():
        simple_row_dict = {}  # type: Dict[str, int]

        for column_label, cell in row_dict.items():
            cell_sample_count = len(cell)

            if cell_sample_count > 0:
                simple_row_dict[column_label] = cell_sample_count

        smpl_conf_dict[row_label] = simple_row_dict

    return smpl_conf_dict


def print_confusion_matrix(confusion_dict: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]],
                           proposed_label_list: List[str] = None) -> None:
    """
    Print the confusion matrix. This method also serves as an example of how to use the sparse confusion matrix.

    :param confusion_dict: The sparse confusion matrix stored as a dict of dicts.
    :param proposed_label_list: The proposed order and subset of class labels to use.
    """
    print()
    print("label_list:", proposed_label_list)
    print()

    # Generate the proposed label list if none provided.
    if proposed_label_list is None:
        row_label_set = set()  # type: Set[str]
        column_label_set = set()  # type: Set[str]

        for row_label, row_dict in confusion_dict.items():
            row_label_set.add(row_label)

            for column_label, _ in row_dict.items():
                column_label_set.add(column_label)

        proposed_label_list = list(row_label_set.union(column_label_set))
        proposed_label_list.sort()

    # Calculate the row and column totals.
    row_total_dict = {}  # type: Dict[str, int]
    column_total_dict = {}  # type: Dict[str, int]

    for row_label, row_dict in confusion_dict.items():
        if row_label in proposed_label_list:
            row_total = 0

            for column_label, cell in row_dict.items():
                if column_label in proposed_label_list:
                    cell_len = len(cell)
                    row_total += cell_len
                    column_total = column_total_dict.get(column_label, 0) + cell_len
                    column_total_dict[column_label] = column_total

            row_total_dict[row_label] = row_total

    # Print the recall confusion matrix
    print("===")
    print("Recall Confusion Matrix:")
    for column_label in proposed_label_list:
        print(column_label[:min(len(column_label), 5)], ".\t", end='')
    print()

    diag_total = 0.0
    diag_count = 0

    for row_label in proposed_label_list:
        row_dict = confusion_dict.get(row_label, {})

        row_total = row_total_dict.get(row_label, 0)

        for column_label in proposed_label_list:
            if row_total > 0:
                cell = row_dict.get(column_label, [])
                count = len(cell)
                print('\033[%dm' % int(37.0 - round((count / row_total) * 7)), end='')
                print(round(count / row_total, 3), "\t", end='')

                if (column_label != '_nc') and (column_label == row_label):
                    diag_total += count / row_total
                    diag_count += 1
            else:
                print('\033[0m', end='')
                print('--- \t', end='')

        print('\033[0m')

    print(f"AVRG = {diag_total / diag_count}")
    print("===")
    print()

    # Print the precision confusion matrix
    print("===")
    print("Precision Confusion Matrix:")
    for column_label in proposed_label_list:
        print(column_label[:min(len(column_label), 5)], ".\t", end='')
    print()

    diag_total = 0.0
    diag_count = 0

    for row_label in proposed_label_list:
        row_dict = confusion_dict.get(row_label, {})

        for column_label in proposed_label_list:
            column_total = column_total_dict.get(column_label, 0)

            if column_total > 0:
                cell = row_dict.get(column_label, [])
                count = len(cell)
                print('\033[%dm' % int(37.0 - round((count / column_total) * 7)), end='')
                print(round(count / column_total, 3), "\t", end='')

                if (column_label != '_nc') and (column_label == row_label):
                    diag_total += count / column_total
                    diag_count += 1
            else:
                print('\033[0m', end='')
                print('--- \t', end='')

        print('\033[0m')

    print(f"AVRG = {diag_total / diag_count}")
    print("===")
    print()


def analyse_clsfr_results(result_list: List[Tuple[str, str, List[str], Optional[str]]]) -> \
        Tuple[float, float, Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]]:
    """
    Analyse the classifier results.

    :param result_list: is a list of results tuples (image, true_label and predicted_labels/top-n-labels)
    :return: The classifier accuracy, f1 score and confusion matrix.
    """
    labels_true = []  # type: List[str]
    labels_predicted = []  # type: List[str]
    num_matched = 0

    # Sparse confusion matrix ...
    confusion_dict = {}  # type: Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]

    if len(result_list) > 0:
        count = 0

        for result_sample in result_list:
            image = result_sample[0]
            true_label = result_sample[1]  # the matrix row label
            predicted_result_labels = result_sample[2]
            sample_uuid = result_sample[3]

            if len(predicted_result_labels) > 0:
                predicted_label = predicted_result_labels[0]  # the matrix column label
            else:
                predicted_label = '_nc'

            row_dict = confusion_dict.get(true_label, {})

            cell = row_dict.get(predicted_label)

            if cell is None:
                cell = [(image, sample_uuid)]
            else:
                cell.append((image, sample_uuid))

            row_dict[predicted_label] = cell
            confusion_dict[true_label] = row_dict

            # === Update the global scoring ===
            # if true_label == predicted_label:
            if true_label in predicted_result_labels:
                num_matched += 1

            labels_true.append(true_label)
            labels_predicted.append(predicted_label)
            # === ===

            # if count % 100 == 0:
            #     print(".", end="", flush=True)
            count += 1

        accuracy = num_matched / len(result_list)
        f1 = sklearn.metrics.f1_score(labels_true, labels_predicted, average='weighted')
        # print(".")

        return accuracy, f1, confusion_dict
    else:
        return 0.0, 0.0, {}


# =========================================================================
# =========================================================================
# =========================================================================

# =========================================================================
# === Load & Save helpers =================================================
# =========================================================================
def save_blob(name: str, blob: Any,
              use_data_folder: bool) -> bool:
    """
    Save the model blob to the storage system.

    :param name: The name of the model to save e.g.
    :param blob:
    :param use_data_folder:
    :return:
    """
    if blob is None:
        return False

    blob.uuid = str(uuid.uuid4())  # Update the uuid of the local copy.

    if use_data_folder:
        try:
            # Save a model to the data folder.
            # logging.info("    save_blob: Saving %s to data folder..." % name)
            file_handle = open(nlp_engine_data.get_path() + '/' + name, 'wb')
            pickle.dump(blob, file_handle, protocol=pickle.HIGHEST_PROTOCOL)
            file_handle.close()
            return True
        except IOError as e:
            logging.error(f"engine_utils.save_blob: {name} IOError {e}!")
            db.session.rollback()
            return False
    else:
        try:
            # Save a model to the DB.
            # logging.info("    save_blob: Dumping %s to blob..." % name)
            handle = io.BytesIO()
            pickle.dump(blob, handle, protocol=feersum_nlu_pickle_protocol_version)

            instance = SDKBlobData.query.get(ident=name)

            if instance:
                instance.blob = handle.getvalue()
                instance.uuid = blob.uuid  # Update the uuid in the DB with the blob's uuid.
            else:
                instance = SDKBlobData(_name=name, _blob=handle.getvalue(),
                                       _uuid=blob.uuid)
                db.session.add(instance)

            # logging.info("    save_blob: Committing %s to DB..." % name)
            db.session.commit()

            handle.close()
            return True
        except InvalidRequestError as error_message:
            logging.error(f"engine_utils.save_blob: {name} InvalidRequestError {error_message}!")
            db.session.rollback()
            return False
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()


def load_blob(name: str,
              use_data_folder: bool,
              cached_blob: Optional[Any]) -> Optional[Any]:
    """
    Load the model blob from the storage system. Returns the blob.
    """
    try:
        if use_data_folder:
            # Load the blob from data folder if not already cached.
            if cached_blob is None:
                # Load a model from the data folder.
                # logging.info("    load_blob: Reading %s from data folder (cache none)." % name)

                file_handle = open(nlp_engine_data.get_path() + '/' + name, 'rb')
                blob = pickle.load(file_handle)
                file_handle.close()
            else:
                # Note: The data folder should be static so assume that any cached model (loaded from
                # either the data folder or the DB) is the latest!
                blob = cached_blob
        else:
            query = db.session.query(SDKBlobData)

            if cached_blob is not None:
                # Make a new query that just returns the uuid column to check if the cached_blob is fresh.
                query = query.options(load_only("uuid"))
                instance_is_partial = True
            else:
                instance_is_partial = False

            instance = query.get(ident=name)

            if instance is not None:
                # === Get blob (either from the instance or from the cache) ===
                if (cached_blob is not None) and (cached_blob.uuid == instance.uuid):
                    # UUID of cache is same as DB instance so reuse cached value.

                    blob = cached_blob
                else:
                    # UUID of DB instance is fresh or cached_blob is None so get full object from DB.

                    if instance_is_partial:
                        # Get full object
                        query = db.session.query(SDKBlobData)
                        instance = query.get(ident=name)

                    handle = io.BytesIO(instance.blob)

                    # if cached_blob is None:
                    #     logging.info("    load_blob: Loading %s from instance.blob (cache stale)." % name)
                    # else:
                    #     logging.info("   load_blob: Loading %s from instance.blob (cache none)." % name)

                    blob = pickle.load(handle)
                    handle.close()
                # === ===
            else:
                logging.info(f"   load_blob: {name} not found!")
                blob = None

    except IOError as e:
        db.session.rollback()
        logging.error(f"load_instance_meta_info_blob: {name} IOError {e}!")
        blob = None
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return blob


def trash_blob(name: str, use_data_folder: bool) -> Optional[Any]:
    """
    Mark the blob as trashed in the storage system.
    """
    # Note: The blobs have no trashed flag like the meta_info_blobs in the service wrapper layer. If the meta info was
    # marked as 'trashed' then the associated blob is also assumed to be trashed.
    #
    # if not use_data_folder:
    #     try:
    #         instance = SDKBlobData.query.get(ident=name)
    #
    #         if instance:
    #             instance.trashed = True
    #             db.session.commit()
    #             success = True
    #         else:
    #             success = False
    #     except Exception:
    #         db.session.rollback()
    #         raise
    #     finally:
    #         db.session.close()
    #
    #     return success
    # else:
    #     # NOTE: Blobs in the data folder ('use_data_folder') cannot be marked as trashed!
    #     return False
    return True


def vaporise_blob(name: str, use_data_folder: bool) -> Optional[Any]:
    """
    Permanently delete the blob in the storage system.
    """
    if not use_data_folder:
        try:
            instance = SDKBlobData.query.get(ident=name)

            if instance:
                db.session.delete(instance)
                db.session.commit()
                success = True
            else:
                success = False

            # # NOTE: Blobs in the data folder ('use_data_folder') are not vaporised!

            return success
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()
    else:
        return False


def save_model(name: str, use_data_folder,
               model_extension: str, model_dict: Dict) -> bool:
    """
    Save the model.
    """
    blobname = name + model_extension
    model = model_dict.get(name)

    if model is not None:
        return save_blob(name=blobname,
                         blob=model,
                         use_data_folder=use_data_folder)
    else:
        return False


def load_model(name: str, use_data_folder: bool,
               model_extension: str, model_dict: Dict) -> bool:
    """
    Load or reload the model instance from the database.
    """
    blobname = name + model_extension
    obj = load_blob(name=blobname,
                    use_data_folder=use_data_folder,
                    cached_blob=model_dict.get(name))

    if obj is not None:
        # ToDo: In general, there needs to be a way of loading not the object, but just its data and re-instantiating a
        #       fresh object with each load. Otherwise, for example, old code and class definitions are dragged
        #       along forever!!!!
        model_dict[name] = obj
        return True
    else:
        # Model not available so delete from local cache and return failure.
        if model_dict.get(name) is not None:
            del model_dict[name]
        return False


def trash_model(name: str, trash_cache_only: bool,
                model_extension: str, model_dict: Dict) -> bool:
    """
    Unload from memory and trash the blob in storage system.
    """
    if not trash_cache_only:
        blobname = name + model_extension
        trash_blob(name=blobname, use_data_folder=False)

    if model_dict.get(name) is not None:
        del model_dict[name]
        return True
    else:
        return False


def vaporise_model(name: str,
                   model_extension: str, model_dict: Dict) -> bool:
    """
    Unload from memory and permanently delete the blob in storage system.
    """
    blobname = name + model_extension
    vaporise_blob(name=blobname, use_data_folder=False)

    if model_dict.get(name) is not None:
        del model_dict[name]
        return True
    else:
        return False


# =========================================================================
# =========================================================================
# =========================================================================


def cnvrt_svfile_to_tuples(file_name: str,
                           value_delimiter=',',
                           rows_to_skip=0) -> List[Tuple[str, str]]:
    """Convert TSV/CSV file of labeled strings to list of tuples.

    :param value_delimiter: The
    :param file_name: The file name of the file.
    :param rows_to_skip: Number of row to skip at the beginning of the file. Set equal to 1 to skip column heading.
    :return: The list of labeled strings.
    """

    list_text = []

    with open(file_name, newline='') as csvfile:
        csvdoc = csv.reader(csvfile, delimiter=value_delimiter, quotechar='"')
        for row in islice(csvdoc, rows_to_skip, None):
            text = row[0]
            class_label = row[1]
            list_text.append((text, class_label))

    return list_text


def cleanup_text(input_text: str) -> str:
    """
    Apply some basic cleanup to the input text. NOTE: Only used by the LID_ZA model.

    :param input_text: The input text.
    :return: The cleaned input text
    """

    text = input_text.lower()
    punc_to_remove = string.punctuation.replace('-', '') + '0123456789'
    text = text.translate(str.maketrans(punc_to_remove, ' ' * len(punc_to_remove)))

    text = text.replace('ã…â¡', 'š')
    text = text.replace('ï¿½', '')
    text = text.replace('ª', '')

    text = " ".join(text.split())
    text = text.strip()

    # All special characters are kept.
    return text
