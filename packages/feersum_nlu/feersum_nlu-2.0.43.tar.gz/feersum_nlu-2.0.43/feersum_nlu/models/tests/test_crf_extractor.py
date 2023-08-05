import unittest
from typing import List, Dict  # noqa # pylint: disable=unused-import

from feersum_nlu.models import crf_extractor

from feersum_nlu.models.tests import BaseTestCase

# References
# - http://www.albertauyeung.com/post/python-sequence-labelling-with-crf/


def calc_accuracy(extr, samples_crf: List[crf_extractor.CRFSample]) -> float:
    sample_acc_total = 0.0
    sample_count = 0

    for sample in samples_crf:
        pred_entity_list, pred_lang_code = extr.predict(sample.text, None)
        sample_acc_total += extr.score_prediction(pred_entity_list=pred_entity_list,
                                                  true_entity_list=sample.entity_list,
                                                  text=sample.text)
        sample_count += 1

    return sample_acc_total / sample_count if (sample_count > 0) else 0.0


# @unittest.skip("skipping during dev")
class TestCRFExtractor(BaseTestCase):
    def test_crf_extractor(self):
        print("Testing TestCRFExtractor.test_crf_extractor ...", flush=True)

        # print(nltk.help.upenn_tagset())

        extr = crf_extractor.CRFExtractor()

        training_samples_json = [
            {"text": "Can I have a burger with chips please?", "entity_list": [{"index": 13, "len": 17, "entity": "food"}]},
            {"text": "Can I have a slice of pizza?", "entity_list": [{"index": 13, "len": 14, "entity": "food"}]},
            {"text": "Can I have a hot dog with mustard?", "entity_list": [{"index": 13, "len": 20, "entity": "food"}]},
            {"text": "Can I have a juice please?", "entity_list": [{"index": 13, "len": 5, "entity": "drink"}]},
            {"text": "Can I have a bottle of water?", "entity_list": [{"index": 13, "len": 15, "entity": "drink"}]},
            {"text": "Can I have a some coffee?", "entity_list": [{"index": 18, "len": 6, "entity": "drink"}]},
        ]

        testing_samples_json = [
            {"text": "Can I have a burger with chips please?", "entity_list": [{"index": 13, "len": 17, "entity": "food"}]},
            {"text": "Can I have a glass of water please?", "entity_list": [{"index": 13, "len": 14, "entity": "drink"}]},
        ]

        training_samples_crf = crf_extractor.CRFExtractor.cnvrt_json_to_crf_samples(training_samples_json)
        testing_samples_crf = crf_extractor.CRFExtractor.cnvrt_json_to_crf_samples(testing_samples_json)

        extr.train(training_samples_crf, testing_samples_crf)

        # Some random tests.
        self.assertTrue(extr.predict("I would like to buy a beef sandwich with mustard.", None)[0][0].entity == 'food')
        self.assertTrue(extr.predict("I would like to buy an ice cream please kind sir.", None)[0][0].entity == 'drink')
        self.assertTrue(extr.predict("Do you have water for me please.", None)[0][0].entity == 'drink')

        # Accuracy test.
        training_accuracy = calc_accuracy(extr, training_samples_crf)
        print("training_accuracy =", training_accuracy, flush=True)
        self.assertTrue(training_accuracy == 1.0)

        # Accuracy test.
        testing_accuracy = calc_accuracy(extr, testing_samples_crf)
        print("testing_accuracy =", testing_accuracy, flush=True)
        self.assertTrue(testing_accuracy == 1.0)

        print()
        print("done.")


if __name__ == '__main__':
    unittest.main()
