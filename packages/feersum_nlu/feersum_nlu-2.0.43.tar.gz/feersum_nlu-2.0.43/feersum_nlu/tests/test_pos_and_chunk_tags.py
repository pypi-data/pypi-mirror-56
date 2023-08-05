# import unittest
# import time
#
# import nltk
#
# from feersum_nlu import nlp_engine
# from feersum_nlu import nlp_engine_data
# from feersum_nlu.models.text_classifier_naive_bayes import TextClassifier
# from feersum_nlu.tests import BaseTestCase
#
#
# # @unittest.skip("skipping during dev")
# class TestTags(BaseTestCase):
#     def test_tags(self):
#         print("Testing TestTags.test_sample.", flush=True)
#
#         start_time = time.time()
#         nlpe = nlp_engine.NLPEngine(use_duckling=False)
#
#         sentence_to_tag = "Die doel van die webtuiste vir Suid-Afrikaanse Regeringsdienste is om 'n enkele bron " \
#                           "van inligting te bied."
#
#         # ===================
#         # ===================
#         # === POS tagging ===
#         pos_tagged_sentences = TextClassifier.cnvrt_ctext_posfile_to_tagged_sentences(
#             nlp_engine_data.get_path() + '/' + 'pos_af_GOV-ZA.csv')
#         # print('pos_tagged_sentences[0] = ', end='')
#         # print(pos_tagged_sentences[0])
#
#         pos_training_set_size = int(len(pos_tagged_sentences) * 4 / 5)
#         pos_tagged_sentences_train = pos_tagged_sentences[:pos_training_set_size]
#         pos_tagged_sentences_test = pos_tagged_sentences[pos_training_set_size:]
#
#         nlpe.train_pos_tagger('gov_za_af', pos_tagged_sentences_train)
#         print('POS accuracy = ', end='')
#         print(nlpe.test_pos_tagger('gov_za_af', pos_tagged_sentences_test))
#         nlpe.save_pos_tagger('gov_za_af')
#
#         nlpe.load_pos_tagger('gov_za_af')
#
#         pos_tags = nlpe.retrieve_pos_tags('gov_za_af', nltk.word_tokenize(sentence_to_tag))
#         pos_tags_null = nlpe.retrieve_pos_tags('gov_za_unknown', nltk.word_tokenize(sentence_to_tag))
#
#         self.assertEqual(pos_tags, [('Die', 'LB'),
#                                     ('doel', 'NSE'),
#                                     ('van', 'SVS'),
#                                     ('die', 'LB'),
#                                     ('webtuiste', 'NSE'),
#                                     ('vir', 'SVS'),
#                                     ('Suid-Afrikaanse', 'ASA'),
#                                     ('Regeringsdienste', 'NSM'),
#                                     ('is', 'VTHOK'),
#                                     ('om', 'SVS'),
#                                     ("'", 'ZPR'),
#                                     ('n', 'UPW'),
#                                     ('enkele', 'THAO'),
#                                     ('bron', 'VTHOO'),
#                                     ('van', 'SVS'),
#                                     ('inligting', 'NM'),
#                                     ('te', 'UPI'),
#                                     ('bied', 'VTHOG'),
#                                     ('.', 'ZE')])
#
#         # Test the use of an unknown instance name.
#         self.assertEqual(pos_tags_null, [])
#
#         # =====================
#         # =====================
#         # === Chunk tagging ===
#         phrase_tagged_sentences = TextClassifier.cnvrt_ctext_phrasefile_to_tagged_sentences(
#             nlp_engine_data.get_path() + '/' + 'chunk_af_NCHLT-phrases.csv')
#
#         sentences = []
#         for phrase_tagged_sentence in phrase_tagged_sentences:
#             sentence = []
#             for (word, phrase_tag) in phrase_tagged_sentence:
#                 sentence.append(word)
#             sentences.append(sentence)
#         # print('sentences[0] = ', end='')
#         # print(sentences[0])
#
#         # Generate POS tag the sentences for training.
#         pos_tagged_sentences = []
#         for sentence in sentences:
#             pos_tagged_sentence = nlpe.retrieve_pos_tags('gov_za_af', sentence)
#             pos_tagged_sentences.append(pos_tagged_sentence)
#         # print('pos_tagged_sentences[0] = ', end='')
#         # print(pos_tagged_sentences[0])
#
#         # Train the chunker with sentences tagged with both POS and IOB phrase chunks.
#         dual_tagged_sentences = nlpe.prepare_dual_tagged_sentences(pos_tagged_sentences, phrase_tagged_sentences)
#         chunk_training_set_size = int(len(dual_tagged_sentences) * 4 / 5)
#         dual_tagged_sentences_train = dual_tagged_sentences[:chunk_training_set_size]
#         dual_tagged_sentences_test = dual_tagged_sentences[chunk_training_set_size:]
#
#         nlpe.train_chunk_tagger('gov_za_af', dual_tagged_sentences_train)
#         print('Chunk accuracy = ', end='')
#         print(nlpe.test_chunk_tagger('gov_za_af', dual_tagged_sentences_test))
#         nlpe.save_chunk_tagger('gov_za_af')
#
#         nlpe.load_chunk_tagger('gov_za_af')
#
#         chunk_tags = nlpe.retrieve_chunk_tags('gov_za_af',
#                                               nlpe.retrieve_pos_tags('gov_za_af', nltk.word_tokenize(sentence_to_tag)))
#
#         end_time = time.time()
#         print('NLPEngine() time = ' + str(end_time - start_time), flush=True)
#         print('[Feersum NLU version = ' + nlp_engine.get_version() + ']', flush=True)
#         print('[NLPEngine data path = ' + nlp_engine_data.get_path() + ']', flush=True)
#         print()
#
#         self.assertEqual(chunk_tags, [('Die', 'LB', 'B-NOUN'),
#                                       ('doel', 'NSE', 'I-NOUN'),
#                                       ('van', 'SVS', 'B-PREP'),
#                                       ('die', 'LB', 'B-NOUN'),
#                                       ('webtuiste', 'NSE', 'I-NOUN'),
#                                       ('vir', 'SVS', 'B-PREP'),
#                                       ('Suid-Afrikaanse', 'ASA', 'B-NOUN'),
#                                       ('Regeringsdienste', 'NSM', 'I-NOUN'),
#                                       ('is', 'VTHOK', 'B-VERB'),
#                                       ('om', 'SVS', 'B-PREP'),
#                                       ("'", 'ZPR', 'OUT'),
#                                       ('n', 'UPW', 'B-NOUN'),
#                                       ('enkele', 'THAO', 'B-NOUN'),
#                                       ('bron', 'VTHOO', 'B-VERB'),
#                                       ('van', 'SVS', 'B-PREP'),
#                                       ('inligting', 'NM', 'B-NOUN'),
#                                       ('te', 'UPI', 'B-VERB'),
#                                       ('bied', 'VTHOG', 'I-VERB'),
#                                       ('.', 'ZE', 'OUT')])
#
#
# #         self.assertTrue(nlpe.purge_chunk_tagger("gov_za_af"))
# #         self.assertTrue(nlpe.purge_pos_tagger("gov_za_af"))
#
#
# if __name__ == '__main__':
#     unittest.main()
