import time
import unittest

from feersum_nlu import vision_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase

from feersum_nlu.image_utils import load_image


# @unittest.skip("skipping during dev")
class TestImageRead(BaseTestCase):
    def test_read(self):
        print("Testing TestImageRead.test_read.", flush=True)

        vise = vision_engine.VisionEngine()

        start_time = time.time()

        image_str = load_image(nlp_engine_data.get_path() + "/vision/disc5.jpg", ignore_resolution=True)
        print(f"Image is {len(image_str)/1024} kB")

        text_list = vise.retrieve_image_text("generic", image_str)

        print(text_list)

        end_time = time.time()

        print('VisionEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum Vision version = ' + vision_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        # self.assertTrue(accuracy > 0.8)


if __name__ == '__main__':
    unittest.main()
