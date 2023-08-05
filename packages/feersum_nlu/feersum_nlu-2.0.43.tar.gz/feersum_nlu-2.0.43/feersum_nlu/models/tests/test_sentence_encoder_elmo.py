import unittest

from feersum_nlu.models import sentence_encoder_elmo

import numpy as np
import time

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSentenceEncoderElmo(BaseTestCase):

    def test(self):
        print("Testing TestSentenceEncoderUSent.test ...", flush=True)

        # First time the model loads the model might have to be retrieved from the hub.
        encoder_load_start_time = time.time()
        encoder = sentence_encoder_elmo.SentenceEncoderElmo("https://tfhub.dev/google/elmo/2?"
                                                            "tf-hub-format=compressed")
        encoder_load_end_time = time.time()
        print('(encoder_load_end_time-encoder_load_start_time)', (encoder_load_end_time-encoder_load_start_time), flush=True)

        encoder_load_start_time = time.time()
        encoder = sentence_encoder_elmo.SentenceEncoderElmo("https://tfhub.dev/google/elmo/2?"
                                                            "tf-hub-format=compressed")
        encoder_load_end_time = time.time()
        print('(encoder_load_end_time-encoder_load_start_time)', (encoder_load_end_time-encoder_load_start_time), flush=True)

        self.assertTrue((encoder_load_end_time-encoder_load_start_time) < 40.0)

        # ===
        self.assertTrue(encoder is not None)
        self.assertTrue(encoder.is_created())

        if encoder is not None:

            # First call might be slow.
            encode_start_time = time.time()
            text_vector = encoder.calc_sentence_vector("Test sentence for word manifold", False)
            encode_end_time = time.time()
            print('(encode_end_time-encode_start_time)', (encode_end_time-encode_start_time), flush=True)

            encode_start_time = time.time()
            text_vector = encoder.calc_sentence_vector("Test sentence for word manifold", False)
            encode_end_time = time.time()
            print('(encode_end_time-encode_start_time)', (encode_end_time-encode_start_time), flush=True)

            self.assertTrue(text_vector.shape[0] == 1024)

            ref_text_vector = np.array([-0.0027589246,  -0.1239867,  -0.060851384,  -0.21573195,
                                        -0.0731933, 0.42711696, -0.3474689, 0.36898148,
                                        0.2017049,  -0.040619444, -0.10582776,  -0.060723554])

            self.assertTrue(np.allclose(text_vector[:12],
                                        ref_text_vector,
                                        rtol=1e-03))

            self.assertTrue((encode_end_time-encode_start_time) < 0.4)


if __name__ == '__main__':
    unittest.main()
