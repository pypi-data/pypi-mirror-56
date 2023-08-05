import time
import unittest

from feersum_nlu import vision_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu import engine_utils

from feersum_nlu.tests import BaseTestCase

from feersum_nlu.image_utils import get_image_samples


# @unittest.skip("skipping during dev")
class TestImageClassification(BaseTestCase):
    def test_accuracy(self):
        print("Testing TestImageClassification.test_accuracy.", flush=True)

        vise = vision_engine.VisionEngine()

        start_time = time.time()

        train_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/train"
        test_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/test"

        training_list = get_image_samples(train_data_path, "cat")
        training_list.extend(get_image_samples(train_data_path, "dog"))

        testing_list = get_image_samples(test_data_path, "cat")
        testing_list.extend(get_image_samples(test_data_path, "dog"))

        vise.train_image_clsfr('test_image_classification',
                               training_list, testing_list,
                               clsfr_algorithm="resnet152",
                               num_epochs=15)  # 10 epochs used for quick testing.

        # vise.save_image_clsfr("test_image_classification")
        # vise.load_image_clsfr("test_image_classification")

        accuracy, f1, cm, cm_labels = vise.test_image_clsfr('test_image_classification', testing_list, 1.0, 1)
        smpl_cm = engine_utils.smplfy_confusion_matrix(cm)

        print("accuracy, f1, smpl_cm, cm_labels =", accuracy, f1, smpl_cm, cm_labels)
        print()

        ret1 = vise.retrieve_image_class('test_image_classification', testing_list[0][0], 1.0, 2)
        print(ret1)

        ret2 = vise.retrieve_image_class('test_image_classification', testing_list[12][0], 1.0, 2)
        print(ret2)

        end_time = time.time()

        print('VisionEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum Vision version = ' + vision_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        print("accuracy = ", accuracy)
        print("ret1[0][0] = ", ret1[0][0])
        print("ret2[0][0] = ", ret2[0][0])

        # Test small training set accuracy and some samples.
        self.assertTrue(accuracy > 0.7)  # 10 epochs is not enough to ensure a high accuracy. Occasionally acc will be ~ 0.75
        self.assertTrue(ret1[0][0] == "cat")
        self.assertTrue(ret2[0][0] == "dog")


if __name__ == '__main__':
    unittest.main()
