import unittest

from data_structures.nlp import Token


class TestToken(unittest.TestCase):

    def test_split_without_meta_attributes(self):
        los_angeles = Token(
            text='Los Angeles',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False)
        los, angeles = los_angeles.split(' ')
        expected_los = Token(
            text='Los',
            pos=None,
            lemma=None,
            is_entity=None,
            entity_type=None,
            is_stop=None)
        self.assertEqual(expected_los, los)
        expected_angeles = Token(
            text='Angeles',
            pos=None,
            lemma=None,
            is_entity=None,
            entity_type=None,
            is_stop=None)
        self.assertEqual(expected_angeles, angeles)

    def test_split_with_meta_attributes(self):
        los_angeles = Token(
            text='Los Angeles',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False)
        los, angeles = los_angeles.split(' ', copy_meta_attrs=True)
        expected_los = Token(
            text='Los',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False)
        self.assertEqual(expected_los, los)
        expected_angeles = Token(
            text='Angeles',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False)
        self.assertEqual(expected_angeles, angeles)
