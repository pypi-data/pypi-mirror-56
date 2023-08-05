import unittest
import pandas as pd
import datetime
from itertools import zip_longest

from feersum_nlu import nlp_engine_data

from feersum_nlu.models import sentence_encoder_usent
from feersum_nlu.models import text_classifier_nn_cosine

from sklearn.model_selection import train_test_split

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestTextClassifierNNVCosineUsent(BaseTestCase):

    # ToDo: Don't download directly from he hub.
    # # Create a folder for the TF hub module.
    # $ mkdir /tmp/moduleA
    # # Download the module, and uncompress it to the destination folder. You might want to do this manually.
    # $ curl -L "https://tfhub.dev/google/universal-sentence-encoder/2?tf-hub-format=compressed" | tar -zxvC /tmp/moduleA
    # # Test to make sure it works.
    # $ python
    # > import tensorflow_hub as hub
    # > hub.Module("/tmp/moduleA")

    def test(self):
        print("Testing TestTextClassifierNNVUsent.test ...", flush=True)

        print("Loading language model...", end='', flush=True)
        language_model = \
            sentence_encoder_usent.SentenceEncoderUSent("https://tfhub.dev/google/universal-sentence-encoder-large/3?"
                                                        "tf-hub-format=compressed")
        print("done.")

        matcher = text_classifier_nn_cosine.TextClassifierNearestNeighbourCosine({"eng": language_model})
        # ===

        self.assertTrue(matcher is not None)

        if matcher is not None:
            # Get the data
            # This data set has 233 scripted FAQs and 47 unique responses
            ginger_df = pd.read_csv(nlp_engine_data.get_path() + "/FAQ_test_data.csv")

            test_size = 0.2

            ginger_train_df, ginger_test_df = train_test_split(ginger_df, test_size=test_size, random_state=42)

            # #Store pandas.Series object as a list -> train with this
            ans_list_train = ginger_train_df['label'].tolist()  # scripted responses
            ques_list_train = ginger_train_df['text'].tolist()  # scripted FAQs
            lang_list_train = [''] * len(ans_list_train)  # empty string for lang_id
            # Put data into required format
            data_train = [sample for sample in zip_longest(ques_list_train, ans_list_train, lang_list_train)]

            ans_list_test = ginger_train_df['label'].tolist()  # scripted responses
            ques_list_test = ginger_train_df['text'].tolist()  # scripted FAQs
            lang_list_test = [''] * len(ans_list_test)  # empty string for lang_id
            # Put data into required format
            data_test = [sample for sample in zip_longest(ques_list_test, ans_list_test, lang_list_test)]

            print("START TRAINING TEXT CLASSIFIER AT ", datetime.datetime.now().time())
            matcher.train(data_train, data_test)
            print("DONE TRAINING TEXT CLASSIFIER AT ", datetime.datetime.now().time())

            # get query text to test with
            queries = ginger_test_df['text'].tolist()

            # How many predicted responses per query to return
            topn = 1

            pred_labels = []
            pred_scores = []

            # predict responses to test queries.
            for query in queries:
                scored_labels, lang_code = matcher.classify(input_text=query,
                                                            lang_code_hint=None,
                                                            weak_match_threshold=1.0,
                                                            top_n=topn)
                pred_label, score = scored_labels[0]

                pred_labels.append(pred_label)
                pred_scores.append(score)

                print(round(len(pred_labels) / len(queries) * 100.0, 2))

            results_df = pd.DataFrame()
            results_df['queries'] = queries
            results_df['pred_labels'] = pred_labels
            results_df['pred_scores'] = pred_scores

            print(results_df)

            print(pred_labels)

            print(ginger_test_df)

            # Sanity check for encoder functionality
            sanity_query = 'Is this a free service'
            sanity_scored_labels, lang_code = matcher.classify(input_text=sanity_query,
                                                               lang_code_hint=None, weak_match_threshold=1.0, top_n=topn)

            # The prediction with most confidence
            self.assertTrue(sanity_scored_labels[0][0] == "Ginger's weekly recipes are 100% free.")

            correct_count = 0
            sample_count = 0

            for index in range(len(queries)):
                pred_label = results_df.iloc[index]['pred_labels']
                true_label = ginger_test_df.iloc[index]['label']

                if pred_label == true_label:
                    correct_count += 1

                sample_count += 1

            accuracy = correct_count / sample_count

            print("accuracy = ", accuracy)

            # Confirm the accuracy on the test set.
            self.assertTrue(accuracy > 0.5)

            # test that matches below threshold are labelled as such
            no_match_query = 'vini vidi vicci'
            # match_query = 'eat vegetables'

            no_match_labels, lang_code = matcher.classify(input_text=no_match_query,
                                                          lang_code_hint=None,
                                                          weak_match_threshold=0.1,  # deliberately dec threshold
                                                          top_n=topn)

            results = [lab[0] for lab in no_match_labels[:topn]]
            probs = [lab[1] for lab in no_match_labels[:topn]]
            print()
            print('RESULTS:', results)
            print('PROB:', probs)
            self.assertTrue(results == [])


if __name__ == '__main__':
    unittest.main()
