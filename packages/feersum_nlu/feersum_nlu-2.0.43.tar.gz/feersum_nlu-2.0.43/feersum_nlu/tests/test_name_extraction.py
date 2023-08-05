import unittest
import time
import pandas as pd

from feersum_nlu import nlp_engine
from feersum_nlu import nlp_engine_data
from feersum_nlu.tests import BaseTestCase


# @unittest.skip("skipping during dev")
class TestNameExtraction(BaseTestCase):
    def test_sample(self):
        """
        """
        print("Testing TestNameExtraction.test_sample.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        test_samples = {"lc_name": ("ari.", ["Ari"]),
                        "uc_name": ("ARI", ["Ari"]),
                        "lc_fullname": ("john doe", ["John Doe"]),
                        "prepend_name1": ("my name is sbu", ["Sbu"]),
                        "prepend_name2": ("I am named nkosinathi makhatini.", ["Nkosinathi Makhatini"]),
                        "title_name": ("Mrs xolani mkhize", ["Mrs Xolani Mkhize"]),
                        "uncommon_name1": ("Happy", ["Happy"]),
                        "uncommon_name2": ("my name is Justice", ["Justice"])}

        lc_name = nlpe.retrieve_person_name_entities(test_samples["lc_name"][0])
        uc_name = nlpe.retrieve_person_name_entities(test_samples["uc_name"][0])
        lc_fullname = nlpe.retrieve_person_name_entities(test_samples["lc_fullname"][0])
        prepend_name1 = nlpe.retrieve_person_name_entities(test_samples["prepend_name1"][0])
        prepend_name2 = nlpe.retrieve_person_name_entities(test_samples["prepend_name2"][0])
        title_name = nlpe.retrieve_person_name_entities(test_samples["title_name"][0])
        uncommon_name1 = nlpe.retrieve_person_name_entities(test_samples["uncommon_name1"][0])
        uncommon_name2 = nlpe.retrieve_person_name_entities(test_samples["uncommon_name2"][0])

        end_time = time.time()
        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()

        self.assertTrue(lc_name == ["Ari"])
        self.assertTrue(uc_name == ["Ari"])
        self.assertTrue(lc_fullname == ["John Doe"])
        self.assertTrue(prepend_name1 == ["Sbu"])
        self.assertTrue(prepend_name2 == ["Nkosinathi Makhatini"])
        self.assertTrue(title_name == ["Mrs Xolani Mkhize"])
        self.assertTrue(uncommon_name1 == ["Happy"])
        self.assertTrue(uncommon_name2 == ["Justice"])

    def test_accuracy(self):
        """
        """
        print("Testing TestNameExtractionAccuracy.test_sample.", flush=True)

        start_time = time.time()
        nlpe = nlp_engine.NLPEngine(use_duckling=False)

        all_samples = [("ari.", ["Ari"]),
                       ("ARI", ["Ari"]),
                       ("Ari.", ["Ari"]),
                       ("john doe", ["John Doe"]),
                       ("Ntabiseng Gumede", ["Ntabiseng Gumede"]),
                       ("Mrs xolani mkhize", ["Mrs Xolani Mkhize"]),
                       ("my name is Justice", ["Justice"]),
                       ("I am bheki", ["Bheki"]),
                       ("im katlego mpela", ["Katlego Mphela"]),
                       ("i'm siphiwe tshabalala", ["Siphiwe Tshabalala"]),
                       ("my name is sbu vilakazi.", ["Sbu Vilakazi"]),
                       ("I am named nkosinathi makhatini.", ["Nkosinathi Makhatini"]),
                       ("My name is Elton MiddleName Chigumbura.", ["Elton Chigumbura"]),
                       ("My name is Abraham Benjamin de Villiers.", ["Abraham Benjamin De Villiers"]),
                       ("My name is Dr Victor Frankenstein.", ["Dr Victor Frankenstein"]),
                       ("I am Reverend John Edward", ["Reverend John Edward"]),
                       ("I am Robert Downey Jr.", ["Robert Downey Jr."]),
                       ("Harvey Spectre, MBA.", ["Harvey Spectre, MBA"]),
                       ("Fernando is my name", ["Fernando"]),
                       ("My name is Kiernan Forbes but you can call me AKA", ["AKA"]),
                       ("I'm not going to say", ["No Valid Name Found"]),
                       ("Happy", ["Happy"]),
                       ("My name is Happy", ["Happy"]),
                       ("No", ["No"])]

        results_df = pd.DataFrame(columns=["Input Text", "Output Text", "Expected Output", "Result"])

        results_df["Input Text"] = [x[0] for x in all_samples]
        results_df["Output Text"] = [nlpe.retrieve_person_name_entities(input_sample[0]) for input_sample in
                                     all_samples]
        results_df["Expected Output"] = [x[1] for x in all_samples]
        results_df["Result"] = ["Pass" if gen_val == exp_val else "Fail"
                                for gen_val, exp_val in zip(results_df["Output Text"], results_df["Expected Output"])]

        # 1 = all correct, 0 = none correct
        accuracy = results_df['Result'].value_counts()['Pass'] / results_df['Result'].count()

        print(results_df["Output Text"])
        print(results_df["Result"])
        print("Name Extraction Accuracy : {0:.3f}".format(accuracy))

        end_time = time.time()
        print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
        print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
        print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
        print()


if __name__ == '__main__':
    unittest.main()
