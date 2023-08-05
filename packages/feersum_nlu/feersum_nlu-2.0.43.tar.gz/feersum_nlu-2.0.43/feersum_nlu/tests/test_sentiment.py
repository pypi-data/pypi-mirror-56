import unittest
import time

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestSentiment(BaseTestCase):
    def test_sample(self):
        print("Testing TestSentiment.test_sample.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        sentences = [("VADER is smart, handsome, and funny.", 0.84, None),  # positive sentence example
                     ("VADER is smart, handsome, and funny!", 0.85, None),
                     # punctuation emphasis handled correctly (sentiment intensity adjusted)
                     ("VADER is very smart, handsome, and funny.", 0.86, None),
                     # booster words handled correctly (sentiment intensity adjusted)
                     ("VADER is VERY SMART, handsome, and FUNNY.", 0.93, None),  # emphasis for ALLCAPS handled
                     ("VADER is VERY SMART, handsome, and FUNNY!!!", 0.94, None),
                     # combination of signals - VADER appropriately adjusts intensity
                     ("VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!", 0.95, None),
                     # booster words & punctuation make this close to ceiling for score
                     ("VADER is not smart, handsome, nor funny.", -0.75, None),  # negation sentence example
                     ("The book was good.", 0.45, None),  # positive sentence
                     ("At least it isn't a horrible book.", 0.44, None),  # negated negative sentence with contraction
                     ("The book was only kind of good.", 0.39, None),
                     # qualified positive sentence is handled correctly (intensity adjusted)
                     ("The plot was good, but the characters are uncompelling and the dialog is not great.", -0.71, None),
                     # mixed negation sentence
                     ("Today SUX!", -0.55, None),  # negative slang with capitalization emphasis
                     ("Today only kinda sux! But I'll get by, lol", 0.53, None),
                     # mixed sentiment example with slang and constrastive conjunction "but"
                     ("Make sure you :) or :D today!", 0.87, None),  # emoticons handled
                     ("Catch utf-8 emoji such as 💘 and 💋 and 😁", 1.0, None),  # emojis handled
                     ("What about emoticons like :-) :). :)? and :( ?", 0.31, None),  #
                     ("Not bad at all", 0.44, None),  # Capitalized negation
                     ("VADER is smart, handsome, and funny. "
                      "The plot was good, but the characters are uncompelling and the dialog is not great. "
                      "Not bad at all.", -0.62, [0.84, -0.71, 0.44])  # paragraph with sentence sentiment reference.
                     ]

        for sentence, value_ref, detail_list_ref in sentences:
            sentiment_value, sentiment_detail_list = nlpe.retrieve_sentiment(sentence, None)

            print(sentence + " => " + str(sentiment_value))

            if sentiment_detail_list is not None:
                print(sentence + " => " + str(sentiment_detail_list))

                for sentiment_detail in sentiment_detail_list:
                    slice_start = int(sentiment_detail.get('index', 0))
                    slice_end = int(slice_start + sentiment_detail.get('len', 0))
                    print("  " + sentence[slice_start:slice_end])

            print()

            # Test total sentiment.
            if value_ref < 0:
                self.assertTrue(value_ref <= sentiment_value < 0)
            else:
                self.assertTrue(value_ref >= sentiment_value > 0)

            # Test sentiment detail if reference provided.
            if detail_list_ref is not None:
                self.assertTrue(sentiment_detail_list is not None)

                if sentiment_detail_list is not None:
                    self.assertTrue(len(detail_list_ref) == len(sentiment_detail_list))

                    for i, sentiment_detail in enumerate(sentiment_detail_list):
                        if detail_list_ref[i] < 0:
                            self.assertTrue(detail_list_ref[i] < sentiment_detail['value'] < 0)
                        else:
                            self.assertTrue(detail_list_ref[i] > sentiment_detail['value'] > 0)

        end_time = time.time()

        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()


if __name__ == '__main__':
    unittest.main()
