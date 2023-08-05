import unittest
import time
from typing import List  # noqa # pylint: disable=unused-import

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSynonymEntityExtractor(BaseTestCase):
    def test_extractor(self):
        print("Testing TestSynonymEntityExtractor.test_extractor.", flush=True)

        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']')
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']')
        print()

        start_time = time.time()

        training_list = []  # type: List[nlp_engine.SynonymSample]
        testing_list = []  # type: List[nlp_engine.SynonymSample]

        training_list.append(nlp_engine.SynonymSample(_text=None, _entity_list=[
            nlp_engine.SynonymEntity(_entity="drink",
                                     _ignore_word_boundaries=False, _ignore_case=True,
                                     _syn_set=["water", "wine", "beer", "juice"],
                                     _index=None, _len=None,
                                     _value=None),
        ]))

        training_list.append(nlp_engine.SynonymSample(_text=None, _entity_list=[
            nlp_engine.SynonymEntity(_entity="food",
                                     _ignore_word_boundaries=False, _ignore_case=True,
                                     _syn_set=["hot dog", "hamburger", "chips", "fish"],
                                     _index=None, _len=None,
                                     _value=None),
        ]))

        nlpe.train_synonym_extr('test_extractor', training_list, testing_list)

        entities, lang_code = nlpe.retrieve_synonym_entities(name='test_extractor',
                                                             input_text="I would like to buy some chips.",
                                                             lang_code=None, weak_match_threshold=1.0)

        self.assertTrue(len(entities) == 1)
        self.assertTrue(entities[0].get('value') == 'chips')

        end_time = time.time()

        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print()


if __name__ == '__main__':
    unittest.main()
