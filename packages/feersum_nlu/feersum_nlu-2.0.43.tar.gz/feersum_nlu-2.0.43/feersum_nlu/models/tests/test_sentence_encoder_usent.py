import unittest

from feersum_nlu.models import sentence_encoder_usent

import numpy as np
import time

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSentenceEncoderUSent(BaseTestCase):

    def test(self):
        print("Testing TestSentenceEncoderUSent.test ...", flush=True)

        # First time the model loads the model might have to be retrieved from the hub.
        encoder_load_start_time = time.time()
        encoder = sentence_encoder_usent.SentenceEncoderUSent("https://tfhub.dev/google/universal-sentence-encoder-large/3?"
                                                              "tf-hub-format=compressed")
        encoder_load_end_time = time.time()
        print('(encoder_load_end_time-encoder_load_start_time)', (encoder_load_end_time-encoder_load_start_time), flush=True)

        encoder_load_start_time = time.time()
        encoder = sentence_encoder_usent.SentenceEncoderUSent("https://tfhub.dev/google/universal-sentence-encoder-large/3?"
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

            self.assertTrue(text_vector.shape[0] == 512)

            # print(text_vector)

            ref_text_vector = np.array([5.98850474e-02,  4.87331450e-02,  7.72956386e-03, -9.26022977e-02,
                                        -5.80346398e-02, -4.34586927e-02, -6.89253658e-02, -3.26415300e-02,
                                        -3.28237824e-02,  4.61593866e-02, -6.98426962e-02,  1.00167030e-02])

            self.assertTrue(np.allclose(text_vector[:12],
                                        ref_text_vector,
                                        rtol=1e-03))

            self.assertTrue((encode_end_time-encode_start_time) < 0.2)


if __name__ == '__main__':
    unittest.main()
