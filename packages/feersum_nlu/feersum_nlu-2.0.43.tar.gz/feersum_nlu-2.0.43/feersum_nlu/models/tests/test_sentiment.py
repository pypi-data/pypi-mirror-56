import unittest

from feersum_nlu.models import sentiment_analyser

from feersum_nlu.models.tests import BaseTestCase


class TestSentiment(BaseTestCase):

    def test(self):
        print("Testing TestSentiment.test ...", flush=True)

        model = sentiment_analyser.SentimentAnalyser()
        # ===

        sentiment = model.get_vader_sentiment("I ain't happy. I'm feeling glad 👍. "
                                              "I got sunshine in a bag. I'm feeling glad.")
        print(sentiment)

        self.assertTrue(sentiment[0] > 0.6)

        self.assertTrue(sentiment[1] is not None)

        if sentiment[1] is not None:
            self.assertTrue(len(sentiment[1]) == 4)
            self.assertTrue(sentiment[1][0]['value'] < -0.4)


if __name__ == '__main__':
    unittest.main()
