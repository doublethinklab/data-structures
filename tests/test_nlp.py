import unittest

from data_structures.nlp import Sentence, Token


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


class TestSentence(unittest.TestCase):

    def test_get_root_ix(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        root_ix = Sentence._get_root_ix(tokens)
        self.assertEqual(1, root_ix)

    def test_drop_prep_subtree(self):
        tokens = [
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        dropped = sentence._drop_prep_subtree(tokens, 4)
        expected = [
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
        ]
        self.assertEqual(expected, dropped)

    def test_get_subtree(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        subtree, root_ix = sentence._get_subtree(3, tokens)
        expected = [
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        self.assertEqual(3, root_ix)
        self.assertEqual(expected, subtree)

    def test_get_subtree_case_2(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        subtree, root_ix = sentence._get_subtree(4, tokens)
        expected = [
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        self.assertEqual(4, root_ix)
        self.assertEqual(expected, subtree)

    def test_remove_appos_removes_when_appos_is_not_root(self):
        tokens = [
            Token('Sam', ix=0, dependency_head_ix=3, dependency_type='nsubj'),
            Token('my', ix=1, dependency_head_ix=2, dependency_type='poss'),
            Token('brother', ix=2, dependency_head_ix=0, dependency_type='appos'),
            Token('arrived', ix=3, dependency_head_ix=None, dependency_type='root'),
        ]
        sentence = Sentence(tokens)
        dropped = sentence._remove_appos(tokens, 0)
        expected = [
            Token('Sam', ix=0, dependency_head_ix=3, dependency_type='nsubj'),
            Token('arrived', ix=3, dependency_head_ix=None, dependency_type='root'),
        ]
        self.assertEqual(expected, dropped)

    def test_remove_appos_does_not_remove_when_appos_is_root(self):
        tokens = [
            Token('my', ix=1, dependency_head_ix=2, dependency_type='poss'),
            Token('brother', ix=2, dependency_head_ix=0,
                  dependency_type='appos'),
        ]
        sentence = Sentence(tokens)
        dropped = sentence._remove_appos(tokens, 2)
        expected = [
            Token('my', ix=1, dependency_head_ix=2, dependency_type='poss'),
            Token('brother', ix=2, dependency_head_ix=0,
                  dependency_type='appos'),
        ]
        self.assertEqual(expected, dropped)

    def test_split_prep_nps(self):
        tokens = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
            Token('in', ix=4, dependency_head_ix=3, dependency_type='prep'),
            Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
            Token('hat', ix=6, dependency_head_ix=4, dependency_type='pobj'),
        ]
        sentence = Sentence(tokens=tokens)
        np, _ = sentence._get_subtree(3, tokens)
        prep_nps = sentence._split_prep_nps(np)
        expected = [[
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('cat', ix=3, dependency_head_ix=1, dependency_type='dobj'),
        ]]
        self.assertEqual(expected, prep_nps)

    def test_sort_tokens(self):
        tokens = [
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
        ]
        sorted_tokens = Sentence._sort_tokens(tokens)
        expected = [
            Token('I', ix=0, dependency_head_ix=1, dependency_type='nsubj'),
            Token('saw', ix=1, dependency_head_ix=None, dependency_type='root'),
            Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
        ]
        self.assertEqual(expected, sorted_tokens)

    def test_subtree_head_missing_required_noun_true_case(self):
        tokens = [
            Token('a', ix=0, dependency_head_ix=1, dependency_type='det'),
            Token('fair', ix=1, dependency_head_ix=2, dependency_type='whatever'),
            Token('fight', ix=2, dependency_head_ix=None, dependency_type='dobj', pos='UNEXPECTED'),
        ]
        self.assertTrue(Sentence._subtree_head_missing_required_noun(tokens, 2))

    def test_subtree_head_missing_required_noun_false_case(self):
        tokens = [
            Token('a', ix=0, dependency_head_ix=1, dependency_type='det'),
            Token('fair', ix=1, dependency_head_ix=2, dependency_type='whatever'),
            Token('fight', ix=2, dependency_head_ix=None, dependency_type='dobj', pos='NOUN'),
        ]
        self.assertFalse(Sentence._subtree_head_missing_required_noun(tokens, 2))

    def test_get_noun_phrases_with_determiner(self):
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
            [
                Token('a', ix=5, dependency_head_ix=6, dependency_type='det'),
                Token('hat', ix=6, dependency_head_ix=4,
                      dependency_type='pobj'),
            ],
            [
                Token('a', ix=2, dependency_head_ix=3, dependency_type='det'),
                Token('cat', ix=3, dependency_head_ix=1,
                      dependency_type='dobj', pos='NOUN'),
            ],
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
