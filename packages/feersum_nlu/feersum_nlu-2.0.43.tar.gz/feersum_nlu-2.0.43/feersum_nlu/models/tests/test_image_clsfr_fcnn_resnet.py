import unittest
import pickle

from feersum_nlu.models import image_classifier_fcnn
from feersum_nlu.models import image_encoder_resnet

from feersum_nlu import nlp_engine_data

from feersum_nlu.image_utils import get_image_samples

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestImageClassifierFCNNResnet(BaseTestCase):

    def test(self):
        print("Testing TestImageClassifierFCNNResnet.test ...", flush=True)

        print("Loading vision model...", end='', flush=True)
        vision_model = \
            image_encoder_resnet.ImageEncoderResnet()
        print("done.")

        print("Creating ImageClassifierFCNN...", end='', flush=True)
        clsfr = image_classifier_fcnn.ImageClassifierFCNN(vision_model)
        print("done.")
        # ===

        self.assertTrue(clsfr is not None)

        if clsfr is not None:
            # Get the data

            # === SDK test data ===
            train_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/train"
            test_data_path = nlp_engine_data.get_path() + "/vision/cats-vs-dogs/test"

            training_list = get_image_samples(train_data_path, "cat")
            training_list.extend(get_image_samples(train_data_path, "dog"))

            testing_list = get_image_samples(test_data_path, "cat")
            testing_list.extend(get_image_samples(test_data_path, "dog"))

            print("Training ImageClassifierFCNN...", end='', flush=True)
            clsfr.train(training_list, testing_list, num_epochs=15)
            print("done.")

            correct_count = 0
            for image, label in testing_list:
                scored_labels = clsfr.classify(input_image=image, weak_match_threshold=1.0, top_n=2)
                if label == scored_labels[0][0]:
                    correct_count = correct_count + 1
            acc = correct_count / len(testing_list)
            print("acc =", acc)
            self.assertTrue(acc > 0.7)

            with open('data.pickle', 'wb') as file:
                pickle.dump(clsfr, file)
            with open('data.pickle', 'rb') as file:
                clsfr_unpickled = pickle.load(file)

            # Add vision model back after unpickling.
            clsfr_unpickled.set_vision_model(vision_model)

            correct_count = 0
            for image, label in testing_list:
                scored_labels = clsfr_unpickled.classify(input_image=image, weak_match_threshold=1.0, top_n=2)
                if label == scored_labels[0][0]:
                    correct_count = correct_count + 1

            acc_unpickled = correct_count / len(testing_list)
            print("acc_unpickled =", acc_unpickled)
            self.assertTrue(acc_unpickled > 0.7)

            for image, label in testing_list:
                scored_labels = clsfr.classify(input_image=image, weak_match_threshold=1.0, top_n=2)
                print(label, scored_labels)


if __name__ == '__main__':
    unittest.main()
