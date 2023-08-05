import unittest
from typing import List, Dict  # noqa # pylint: disable=unused-import

from feersum_nlu.models import synonym_extractor

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSynonymExtractor(BaseTestCase):
    def test_synonym_extractor(self):
        print("Testing TestSynonymExtractor.test_synonym_extractor ...", flush=True)

        extr = synonym_extractor.SynonymExtractor()

        training_samples_json = []  # type: List[Dict]
        testing_samples_json = []  # type: List[Dict]

        training_samples_json.append({
            "text": "Can I have a burger with chips please?",
            "entity_list":
                [
                    {"index": 13, "len": 6, "entity": "food"},
                    {"index": 25, "len": 5, "entity": "food"}
                ]
        })
        training_samples_json.append({
            "text": "Can I have a slice of pizza?",
            "entity_list":
                [
                    {"index": 22, "len": 5, "entity": "food"}
                ]
        })
        training_samples_json.append({
            "text": "Can I have a hot dog with mustard?",
            "entity_list":
                [
                    {"index": 13, "len": 7, "entity": "food"}
                ]
        })

        training_samples_json.append({
            "text": "Can I have a hot dog with All Gold?",
            "entity_list":
                [
                    {"index": 26, "len": 8, "entity": "sauce", "ignore_case": True},
                    {"index": 26, "len": 8, "entity": "cased_sauce", "ignore_case": False},
                ]
        })

        training_samples_json.append({
            "entity_list":
                [
                    {"entity": "food", "ignore_case": True, "ignore_word_boundaries": True,
                     "syn_set": ['hamburger', 'fish', 'sandwich']},
                    {"entity": "drink", "ignore_case": True, "ignore_word_boundaries": True,
                     "syn_set": ['water', 'wine', 'beer', 'BEER']}
                ]
        })

        training_samples_json.append({
            "entity_list":
                [
                    {"entity": "food", "ignore_case": True, "ignore_word_boundaries": True,
                     "syn_set": ['hamburger', 'fish', 'sandwich']},
                    {"entity": "drink", "ignore_case": True, "ignore_word_boundaries": True,
                     "syn_set": ['water', 'wine', 'beer', 'BEER']}
                ]
        })

        training_samples_synonym = synonym_extractor.SynonymExtractor.cnvrt_json_to_synonym_samples(training_samples_json)
        testing_samples_synonym = synonym_extractor.SynonymExtractor.cnvrt_json_to_synonym_samples(testing_samples_json)

        extr.train(training_samples_synonym, testing_samples_synonym)

        self.assertTrue(extr.predict("I would like to buy a beef sandWiches with mustard.", None)[0][0].entity == 'food')
        print(extr.predict("I would like to buy some beef sandWiches with mustard.", None))

        self.assertTrue(extr.predict("I would like to buy a bottle of Water.", None)[0][0].entity == 'drink')
        print(extr.predict("I would like to buy a bottle of WateR.", None))

        self.assertTrue(extr.predict("Do you sell beer here.", None)[0][0].entity == 'drink')
        print(extr.predict("Do you sell beer here.", None))

        print(extr.predict("Can I have a burger with chips and a burger without?.", None))

        self.assertTrue(extr.predict("Please put All Gold for me.", None)[0][0].entity == 'sauce')
        self.assertTrue(extr.predict("Please put All Gold for me.", None)[0][1].entity == 'cased_sauce')
        print(extr.predict("Please put All Gold for me.", None))

        self.assertTrue(extr.predict("Please put all gold for me.", None)[0][0].entity == 'sauce')
        print(extr.predict("Please put all gold for me.", None))

        print()
        print("done.")


if __name__ == '__main__':
    unittest.main()
