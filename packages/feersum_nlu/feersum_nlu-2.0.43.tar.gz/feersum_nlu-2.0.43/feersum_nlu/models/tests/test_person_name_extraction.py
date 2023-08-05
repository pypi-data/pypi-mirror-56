import unittest
# import time
import pandas as pd
from typing import Optional, List, Tuple  # noqa # pylint: disable=unused-import

from feersum_nlu.models import person_name_extractor as extractor

from feersum_nlu.models.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestPersonNameExtraction(BaseTestCase):
    def test_sample(self):
        """test if the extraction process works for different types of names
        """
        print("Testing TestPersonNameExtraction.test_sample.", flush=True)

        # start_time = time.time()

        test_samples = [("ari.", "Ari"),  # lower case with period
                        ("ARI", "Ari"),  # Upper case with period
                        ("john doe.", "John Doe"),  # lc fullname
                        ("my name is sbu", "Sbu"),  # prepend_name1
                        ("I am named nkosinathi makhatini", "Nkosinathi Makhatini"),  # prepend_name2
                        ("Mrs xolani mkhize", "Mrs Xolani Mkhize"),  # title_name
                        ("Happy", "Happy"),  # uncommon_name1
                        ("my name is Justice", "Justice"),  # uncommon_name2
                        ("My name is Clark Kent.", "Clark Kent"),
                        ("I am Billy.", "Billy"),
                        ("My friends call me Billy", "Billy"),
                        ("My friends call me Billy The Kid", "Billy The Kid"),
                        ("Please call me Billy", "Billy")
                        ]

        results_df = pd.DataFrame(columns=["Input Text", "Output Text", "Expected Output", "Result"])

        results_df["Input Text"] = [x[0] for x in test_samples]
        results_df["Output Text"] = [extractor.PersonNameExtractor(input_sample[0]).retrieve_person_name_entities()
                                     for input_sample in test_samples]
        results_df["Expected Output"] = [x[1] for x in test_samples]
        results_df["Result"] = ["Pass" if gen_val == exp_val else "Fail"
                                for gen_val, exp_val in zip(results_df["Output Text"], results_df["Expected Output"])]

        current_accuracy = 0.69

        if "Pass" in results_df["Result"].values:
            accuracy = results_df['Result'].value_counts()["Pass"] / results_df["Result"].count()
        else:
            accuracy = 0.0

        print(results_df)
        print(accuracy)

        self.assertTrue(round(accuracy, 2) >= current_accuracy)

    def test_global_accuracy(self):
        """  Quantify how well does the extraction work for different types of names
        """
        print("Testing TestNameExtractionAccuracy.test_global_accuracy.", flush=True)

        single_word_samples = [("ari.", "Ari"),  # lower case with period
                               ("ARI", "Ari"),
                               ("Ari.", "Ari"),  # Upper case with period
                               ("Happy", "Happy"),
                               ("No", None),  # in global list of invalid names
                               ("expletive", None),  # in global list of invalid names
                               ("jfdga", None),  # random keyboard strokes
                               ("q", None)  # Single letter name
                               ]  # type: List[Tuple[str, Optional[str]]]

        two_word_samples = [("john doe", "John Doe"),
                            ("Nah ah", None),
                            ("Anthony Ireland", "Anthony Ireland"),
                            ("siphiwe tshabalala", "Siphiwe Tshabalala"),
                            ("Doctor Khumalo", "Doctor Khumalo"),
                            ("fgxh xfgh", None),
                            ("Colonel Mustard", "Colonel Mustard"),
                            ("Ntabiseng Gumede", "Ntabiseng Gumede")
                            ]  # type: List[Tuple[str, Optional[str]]]

        my_name_is_samples = [("my name is Justice", "Justice"),
                              ("my name is sbu vilakazi", "Sbu Vilakazi"),
                              ("My name is Henry Khaaba Olonga", "Henry Khaaba Olonga"),
                              ("My name is Abraham Benjamin de Villiers", "Abraham Benjamin De Villiers"),
                              ("My name is Dr Victor Frankenstein", "Dr Victor Frankenstein"),
                              ("My name is Kiernan Forbes but you can call me AKA", "AKA"),
                              ("My name is Happy", "Happy"),
                              ("Fernando is my name", "Fernando"),
                              ("my name is godknows", "Godknows")
                              ]  # type: List[Tuple[str, Optional[str]]]

        i_am_samples = [("I am bheki", "Bheki"),
                        ("im katlego mphela", "Katlego Mphela"),
                        ("I am named nkosinathi makhatini", "Nkosinathi Makhatini"),
                        ("I am Reverend John Edward", "Reverend John Edward"),
                        ("I am Robert Downey Jr", "Robert Downey Jr"),
                        ("I AM Johan", "Johan"),
                        ("I'm africa", "Africa"),
                        ("I'm not going to say", None)
                        ]  # type: List[Tuple[str, Optional[str]]]

        title_samples = [("Mrs xolani mkhize", "Mrs Xolani Mkhize"),
                         ("Mr Arthur Conan Doyle", "Mr Arthur Conan Doyle"),
                         ("Ms Deloris Umbridge", "Ms Deloris Umbridge"),
                         ("Henry VIII of England", "Henry VIII")
                         ]  # type: List[Tuple[str, Optional[str]]]

        edge_case_samples = [("The day after tomorrow", None),
                             ("The colour green", None),
                             ("My friends call me Harry", "Harry"),
                             ("Sarah-Anne O'Neill", "Sarah-Anne O'Neill"),
                             ("Richard III", "Richard III"),
                             ("Wednesday Addams", "Wednesday Addams"),
                             ("James van der Beek", "James Van Der Beek"),
                             ("Albus Percival Wulfrick Brian  Dumbledore", "Albus Percival Wulfrick Brian  Dumbledore")
                             ]  # type: List[Tuple[str, Optional[str]]]

        all_samples = single_word_samples + two_word_samples + my_name_is_samples + \
            i_am_samples + title_samples + edge_case_samples

        results_df = pd.DataFrame(columns=["Input Text", "Output Text", "Expected Output", "Result"])

        results_df["Input Text"] = [x[0] for x in all_samples]
        results_df["Output Text"] = [extractor.PersonNameExtractor(input_sample[0]).retrieve_person_name_entities()
                                     for input_sample in all_samples]
        results_df["Expected Output"] = [x[1] for x in all_samples]
        results_df["Result"] = ["Pass" if gen_val == exp_val else "Fail"
                                for gen_val, exp_val in zip(results_df["Output Text"], results_df["Expected Output"])]

        current_accuracy = 0.77

        if "Pass" in results_df["Result"].values:
            accuracy = results_df["Result"].value_counts()['Pass'] / results_df['Result'].count()
        else:
            accuracy = 0.0

        self.assertTrue(round(accuracy, 2) >= current_accuracy)


if __name__ == '__main__':
    unittest.main()
