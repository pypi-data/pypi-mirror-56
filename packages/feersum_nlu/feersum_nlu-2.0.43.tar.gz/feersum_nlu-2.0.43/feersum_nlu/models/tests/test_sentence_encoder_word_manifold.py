import unittest
# import os

from feersum_nlu import nlp_engine_data
from feersum_nlu.models import word_manifold

import numpy as np
import time

from feersum_nlu.models.tests import BaseTestCase


class TestSentenceEncoderWordManifold(BaseTestCase):

    def test(self):
        print("Testing TestSentenceEncoderWordManifold.test ...", flush=True)

        local_file_cache_path, blob_file_name = \
            nlp_engine_data.get_blob_from_gcp_bucket('glove_and_fasttext_ref', "glove.6B.50d.trimmed.txt")
        manifold_model_path = f"{local_file_cache_path}/{blob_file_name}"

        encoder_load_start_time = time.time()
        encoder = word_manifold.WordManifold(manifold_model_path)

        encoder_load_end_time = time.time()

        print('(encoder_load_end_time-encoder_load_start_time)', (encoder_load_end_time-encoder_load_start_time))

        self.assertTrue((encoder_load_end_time-encoder_load_start_time) < 15.0)

        # ===
        self.assertTrue(encoder is not None)
        self.assertTrue(encoder.is_created())

        if encoder is not None:

            # First call might be slow.
            encode_start_time = time.time()
            text_vector = encoder.calc_sentence_vector("Test sentence for word manifold", False)
            encode_end_time = time.time()
            print('(encode_end_time-encode_start_time)', (encode_end_time-encode_start_time))

            encode_start_time = time.time()
            text_vector = encoder.calc_sentence_vector("Test sentence for word manifold", False)
            encode_end_time = time.time()
            print('(encode_end_time-encode_start_time)', (encode_end_time-encode_start_time))

            self.assertTrue(text_vector.shape[0] == 50)

            ref_text_vector = np.array([0.22321164, 0.19458654, 0.10974761, 0.12952285, 0.18017747, 0.12926753,
                                        0.31236449, 0.17170606, 0.3131397,  0.18227413, 0.13149911, 0.12183519,
                                        0.24232473, 0.07025953, 0.29474978, 0.13195261, 0.15078704, 0.14953808,
                                        0.28698414, 0.2332046,  0.13159301, 0.15699094, 0.08842885, 0.1512044,
                                        0.20311516, 0.46167095, 0.28477611, 0.31850989, 0.11851572, 0.1934109,
                                        0.81538527, 0.2534422,  0.13344405, 0.08873385, 0.26951754, 0.11817695,
                                        0.29540712, 0.20203805, 0.09924927, 0.32499373, 0.24766856, 0.13684763,
                                        0.12902191, 0.1921462,  0.19519218, 0.2192102,  0.13580854, 0.17342112,
                                        0.10374803, 0.06514481])

            self.assertTrue(np.allclose(text_vector,
                                        ref_text_vector,
                                        rtol=1e-03))

            self.assertTrue((encode_end_time-encode_start_time) < 0.1)


if __name__ == '__main__':
    unittest.main()
