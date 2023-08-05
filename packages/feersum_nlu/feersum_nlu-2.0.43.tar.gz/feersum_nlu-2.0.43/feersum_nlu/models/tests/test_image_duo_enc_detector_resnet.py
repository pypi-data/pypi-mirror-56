import unittest

from feersum_nlu.models import image_duo_encoder_detector_resnet
from feersum_nlu.image_utils import load_image

from feersum_nlu.models.tests import BaseTestCase


@unittest.skip("skipping because the data is not available everywhere.")
class TestImageDetectorMaskRCNNResnet(BaseTestCase):

    def test(self):
        print("Testing TestImageDetectorMaskRCNNResnet.test ...", flush=True)

        print("Creating ImageDetectorMaskRCNNResnet...", end='', flush=True)
        detector = image_duo_encoder_detector_resnet.ImageDuoEncoderDetectorResnet()
        print("done.")
        # ===

        self.assertTrue(detector is not None)

        if detector is not None:
            # Get the data

            # === SDK test data ===
            # train_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/train"
            # test_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/test"
            #
            # training_list = get_image_samples(train_data_path, "cat")
            # training_list.extend(get_image_samples(train_data_path, "dog"))
            #
            # testing_list = get_image_samples(test_data_path, "cat")
            # testing_list.extend(get_image_samples(test_data_path, "dog"))

            print("Training ImageDetectorMaskRCNNResnet...", end='', flush=True)
            detector.train(
                # training_list, testing_list,
                num_epochs=1)
            print("done.")

            test_filename = "/Users/bduvenhage/myWork/dev/Praekelt/feersum-nlu-sdk_develop/" \
                            "feersum_nlu/models/PennFudanPed/PNGImages/FudanPed00001.png"
            test_image = load_image(file_name=test_filename, ignore_resolution=True)

            scored_labels = detector.detect(input_image=test_image, weak_match_threshold=1.0, top_n=10)
            print(scored_labels)

            # with open('data.pickle', 'wb') as file:
            #     pickle.dump(detector, file)
            # with open('data.pickle', 'rb') as file:
            #     detector_unpickled = pickle.load(file)
            #
            # scored_labels = detector_unpickled.classify(input_image=image, weak_match_threshold=1.0, top_n=2)


if __name__ == '__main__':
    unittest.main()
