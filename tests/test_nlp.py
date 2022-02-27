import dill
import unittest

from data_structures.nlp import merge_tokens, Sentence, Token


class TestToken(unittest.TestCase):

    def test_split_without_meta_attributes(self):
        los_angeles = Token(
            text='Los Angeles',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False,
            ix=4,
            dependency_head_ix=1,
            dependency_type='dobj')
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
            is_stop=False,
            ix=4,
            dependency_head_ix=1,
            dependency_type='dobj')
        los, angeles = los_angeles.split(' ', copy_meta_attrs=True)
        expected_los = Token(
            text='Los',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False,
            ix=None,
            dependency_head_ix=1,
            dependency_type='dobj')
        self.assertEqual(expected_los, los)
        expected_angeles = Token(
            text='Angeles',
            pos='NOUN',
            lemma='Los Angel',
            is_entity=True,
            entity_type='CITY',
            is_stop=False,
            ix=None,
            dependency_head_ix=1,
            dependency_type='dobj')
        self.assertEqual(expected_angeles, angeles)


class TestMergeTokens(unittest.TestCase):

    def test_merge_tokens_case_1_do_not_merge_det(self):
        tokens = [
            Token('the', 'DET', 'the', False, '', False, 0, 1, 'det'),
            Token('Los', 'PROPN', 'Los', False, '', False, 1, 2, 'nn'),
            Token('Angeles', 'PROPN', 'Angel', False, '', False, 2, 3, 'nn'),
            Token('Lakers', 'PROPN', 'Laker', False, '', False, 3, 4, 'nsubj'),
        ]
        merged = merge_tokens(tokens, merge_det=False)
        expected = [
            Token('the', 'DET', 'the', False, '', False, 0, 1, 'det'),
            Token('Los Angeles Lakers', 'PROPN', 'Los Angel Laker', False, '',
                  False, 3, 4, 'nsubj'),
        ]
        self.assertEqual(expected, merged)

    def test_merge_tokens_case_1_do_merge_det(self):
        tokens = [
            Token('the', 'DET', 'the', False, '', False, 0, 1, 'det'),
            Token('Los', 'PROPN', 'Los', False, '', False, 1, 2, 'nn'),
            Token('Angeles', 'PROPN', 'Angel', False, '', False, 2, 3, 'nn'),
            Token('Lakers', 'PROPN', 'Laker', False, '', False, 3, 4, 'nsubj'),
        ]
        merged = merge_tokens(tokens, merge_det=True)
        expected = [
            Token('the Los Angeles Lakers', 'PROPN', 'the Los Angel Laker',
                  False, '', False, 3, 4, 'nsubj'),
        ]
        self.assertEqual(expected, merged)


class TestNounPhrases(unittest.TestCase):

    def test_case_1(self):
        with open('temp/prob_doc1.dill', 'rb') as f:
            doc = dill.loads(f.read())
        # TODO: looks like max_len not working?
        error = False
        try:
            doc.get_noun_phrases()
        except Exception as e:
            error = True
            raise e
        self.assertFalse(error)

    def test_case_2(self):
        with open('temp/prob_doc2.dill', 'rb') as f:
            doc = dill.loads(f.read())
        error = False
        try:
            doc.get_noun_phrases()
        except:
            error = True
        self.assertFalse(error)

    def test_get_noun_phrases_with_determiner(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj',
                  pos='NOUN'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        nps = sentence.get_noun_phrases(det=True)
        expected = [
            [
                Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
                Token('cat', ix=3, dependency_head_ix=1,
                      dependency_type='dobj', pos='NOUN'),
                Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
                Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
                Token('hat', ix=6, dependency_head_ix=4,
                      dependency_type='pobj'),
            ],
            # TODO: get these splitting again
            # [
            #     Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            #     Token('hat', ix=6, dependency_head_ix=4,
            #           dependency_type='pobj'),
            # ],
            # [
            #     Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            #     Token('cat', ix=3, dependency_head_ix=1,
            #           dependency_type='dobj', pos='NOUN'),
            # ],
        ]
        self.assertEqual(expected, nps)

    def test_get_noun_phrases_without_determiner(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj', pos='NOUN'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        nps = sentence.get_noun_phrases(det=False)
        expected = [
            [
                Token('cat', ix=3, dependency_head_ix=1,
                      dependency_type='dobj', pos='NOUN'),
                Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
                Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
                Token('hat', ix=6, dependency_head_ix=4,
                      dependency_type='pobj'),
            ],
        ]
        self.assertEqual(expected, nps)


class TestVerbPhrases(unittest.TestCase):

    def test_case_1(self):
        with open('temp/prob_doc1.dill', 'rb') as f:
            doc = dill.loads(f.read())
        # TODO: looks like max_len not working?
        error = False
        try:
            doc.get_verb_phrases()
        except Exception as e:
            error = True
            raise e
        self.assertFalse(error)

    def test_case_2(self):
        with open('temp/prob_doc2.dill', 'rb') as f:
            doc = dill.loads(f.read())
        error = False
        try:
            doc.get_verb_phrases()
        except:
            error = True
        self.assertFalse(error)
