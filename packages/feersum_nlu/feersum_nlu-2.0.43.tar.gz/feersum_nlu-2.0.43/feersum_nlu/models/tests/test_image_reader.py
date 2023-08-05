import unittest
# import pickle

from feersum_nlu.models import image_reader_base
from feersum_nlu import nlp_engine_data

from feersum_nlu.image_utils import load_image

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestImageReader(BaseTestCase):

    def test(self):
        print("Testing TestImageReader.test ...", flush=True)

        image_str = load_image(nlp_engine_data.get_path() + "/vision/disc5.jpg", ignore_resolution=True)
        print(f"Image is {len(image_str)/1024} kB")

        text_list = image_reader_base.ImageReaderBase.read_text(image_str)

        print(text_list)
        # self.assertTrue(scored_labels[0][0] == 'cat')


if __name__ == '__main__':
    unittest.main()
