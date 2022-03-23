import dill
import unittest

from data_structures.nlp import Token, Sentence, Paragraph, Document


class TestTokenSerialization(unittest.TestCase):

    def test_serialization(self):
        los_angeles = Token(
                text='Los Angeles',
                pos='NOUN',
                lemma='Los Angel',
                is_entity=True,
                entity_type='CITY',
                is_stop=False)
        serialized = los_angeles.serialize()
        _los_angeles = dill.loads(serialized)

        self.assertEqual(los_angeles.text, _los_angeles.text)
        self.assertEqual(los_angeles.pos, _los_angeles.pos)
        self.assertEqual(los_angeles.lemma, _los_angeles.lemma)
        self.assertEqual(los_angeles.is_entity, _los_angeles.is_entity)
        self.assertEqual(los_angeles.entity_type, _los_angeles.entity_type)
        self.assertEqual(los_angeles.is_stop, _los_angeles.is_stop)
        self.assertEqual(los_angeles.split(split_on=' '),
                         _los_angeles.split(split_on=' '))


class TestSentence(unittest.TestCase):

    def test_serialization(self):
        pass


class TestDocument(unittest.TestCase):

    def test_serialization(self):
        pass
