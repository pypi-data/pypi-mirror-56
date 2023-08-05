import unittest

from feersum_nlu.models import lid
from feersum_nlu.models.tests import BaseTestCase


class TestLID(BaseTestCase):

    def test(self):
        print("Testing TestLID.test ...", flush=True)

        labels = lid.lang_ident_nbayes("Hierdie boodskap is in afrikaans.")
        print(labels)
        self.assertTrue(labels[0][0] == 'afr')

        labels = lid.lang_ident_nbayes("This message is in english.")
        print(labels)
        self.assertTrue(labels[0][0] == 'eng')


if __name__ == '__main__':
    unittest.main()
