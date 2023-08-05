"""
Feersum_nlu SentimentAnalysis class.
"""

from typing import Tuple, Optional, List, Dict, Union
# from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from itertools import islice

from nltk.data import load
from feersum_nlu import nlp_engine_data
# from nltk.tokenize.punkt import PunktSentenceTokenizer


def sent_span_tokenize(text, language='english') -> List[Tuple[int, int]]:
    """
    :param text: text to split into sentences
    :param language: the model name in the Punkt corpus
    """
    tokenizer = load(f'tokenizers/punkt/{language}.pickle')
    return list(tokenizer.span_tokenize(text))


class SentimentAnalyser(object):
    """ Perform sentiment analysis on text """

    def __init__(self) -> None:
        self.uuid = ""  # Duck typed unique version identifier used for model cache coherence of the SDK level model DB.
        self.analyser = SentimentIntensityAnalyzer()

        self.emoji_sent_dict = {}  # type: Dict[str, float]
        emoji_ranking_filename = nlp_engine_data.get_path() + "/" + "Emoji Sentiment RankingV1/Emoji_Sentiment_Data_v1.0.csv"

        with open(emoji_ranking_filename, newline='') as csvfile:
            csvdoc = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in islice(csvdoc, 1, None):
                emoji = row[0]
                negative = float(row[4])
                neutral = float(row[5])
                positive = float(row[6])
                total = negative + neutral + positive
                sentiment = 1.0 * (positive / total) - 1.0 * (negative / total)
                self.emoji_sent_dict[emoji] = sentiment

    @staticmethod
    def combine_sentiment(vader_sent: float, emoji_sent: float):
        sentiment = vader_sent + emoji_sent

        if sentiment > 1.0:
            sentiment = 1.0
        if sentiment < -1.0:
            sentiment = -1.0

        return sentiment

    def get_emoji_sentiment(self, input_text: str):
        sentiment = 0.0

        for char in input_text:
            sentiment += self.emoji_sent_dict.get(char, 0.0)

        if sentiment > 1.0:
            sentiment = 1.0
        if sentiment < -1.0:
            sentiment = -1.0

        return sentiment

    # ----------------------------------------------------
    def get_vader_sentiment(self, input_text: str,
                            add_emoji_sentiment: bool = True) -> Tuple[float, Optional[List[Dict[str, Union[float, int]]]]]:
        """
        :param input_text: The text to process.
        :param add_emoji_sentiment: Add in emoji character sentiments if True.
        :return: The sentiment value between -1(negative sentiment) and +1(positive sentiment) as well as an optional list
        of sentiment dicts for parts of the input text i.e. [{value, index, len}].
        """

        total_sentiment = self.analyser.polarity_scores(input_text)['compound']
        if add_emoji_sentiment:
            total_sentiment = self.combine_sentiment(vader_sent=total_sentiment,
                                                     emoji_sent=self.get_emoji_sentiment(input_text))

        # Rerun Vader on sentences to test detail interface.
        span_list = sent_span_tokenize(input_text)
        detail_list = []  # type: List[Dict[str, Union[float, int]]]

        for index, stop in span_list:
            sentence = input_text[index:stop]
            length = stop - index

            if length > 1:  # Filter out short sentences that might only be punctuation.
                sub_sentiment = self.analyser.polarity_scores(sentence)['compound']
                if add_emoji_sentiment:
                    sub_sentiment = self.combine_sentiment(vader_sent=sub_sentiment,
                                                           emoji_sent=self.get_emoji_sentiment(sentence))
                detail_list.append({"value": sub_sentiment, "index": index, "len": length})

        # Note: detail_list can also be None if algorithm doesn't provide detailed results!
        return total_sentiment, detail_list
