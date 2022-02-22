from typing import List, Optional, Tuple

import dill

from data_structures import base


class Token:

    def __init__(
            self,
            text: str,
            pos: Optional[str] = None,
            lemma: Optional[str] = None,
            is_entity: Optional[bool] = None,
            entity_type: Optional[str] = None,
            is_stop: Optional[bool] = None,
            ix: Optional[int] = None,
            dependency_head_ix: Optional[int] = None,
            dependency_type: Optional[str] = None
    ):
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.is_entity = is_entity
        self.entity_type = entity_type
        self.is_stop = is_stop
        self.ix = ix
        self.dependency_head_ix = dependency_head_ix
        self.dependency_type = dependency_type

    def __eq__(self, other):
        return base.dict_equal_with_debug(self, other)

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return self.text

    def split(
            self,
            split_on: str,
            copy_meta_attrs: bool = False
    ) -> List:
        if split_on in self.text:
            splits = self.text.split(split_on)
            # TODO: what really makes sense here?
            tokens = [
                Token(
                    text=x,
                    pos=self.pos if copy_meta_attrs else None,
                    lemma=self.lemma if copy_meta_attrs else None,
                    is_entity=self.is_entity if copy_meta_attrs else None,
                    entity_type=self.entity_type if copy_meta_attrs else None,
                    is_stop=self.is_stop if copy_meta_attrs else None)
                for x in splits]
            return tokens
        else:
            return [self]

    def serialize(self):
        return dill.dumps(self)


class Sentence:

    def __init__(
            self,
            tokens: List[Token]
    ):
        self.tokens = tokens

    def __len__(self):
        # number of tokens
        return len(self.tokens)

    def __repr__(self):
        return self.text

    def _get_split_prep_nps(self, np: List[Token]) -> List[List[Token]]:
        prep_nps = []
        preps = [x for x in np if x.dependency_type == 'prep']
        # basically, just add the subtrees for each prep
        for prep in preps:
            subtree, _ = self._get_subtree(prep.ix, np)
            prep_nps.append(subtree)
        return prep_nps

    def _get_subtree(
            self,
            ix: int,
            tokens: List[Token]
    ) -> Tuple[List[Token], int]:
        subtree = []
        root = tokens[ix]
        subtree_root_ix = root.ix
        queue = [root]
        while len(queue) > 0:
            children = [x for x in self.tokens
                        if x.dependency_head_ix == root.ix]
            for child in children:
                subtree.append(child)
                queue.append(child)
            queue.remove(root)
            if len(queue) > 0:
                root = queue[0]
        subtree = self._sort_tokens(subtree)
        return subtree, subtree_root_ix

    def _remove_appos(self, subtree: List[Token], root_ix: int) -> List[Token]:
        # the complication here is that we KEEP appos if it is the root of
        # the subtree

        # next we check for any appos
        appos = [x for x in subtree if x.dependency_type == 'appos']

        # if we have any, we check to see if they are root, if not, remove
        for x in appos:
            if x.ix != root_ix:
                subtree.remove(x)

        # finally, make sure the tokens are sorted correctly before returning
        return self._sort_tokens(subtree)

    @staticmethod
    def _sort_tokens(tokens: List[Token]) -> List[Token]:
        return list(sorted(tokens, key=lambda x: x.ix))

    @staticmethod
    def _subtree_head_missing_required_noun(
            subtree: List[Token],
            root_ix: int
    ) -> bool:
        root = next(x for x in subtree if x.ix == root_ix)
        types_requiring_noun = ['attr', 'cop', 'dobj']
        return root.dependency_type in types_requiring_noun \
               and root.pos != 'NOUN'

    @property
    def entities(self) -> List[Token]:
        return [x for x in self.tokens if x.is_entity]

    @property
    def noun_phrases(self) -> List[List[Token]]:
        nps = []

        # refer to README.md for details and examples
        target_types = [
            'nsubj', 'dobj', 'pobj', 'appos', 'attr', 'cop', 'nsubj',
            'nsubjpass', 'obj', 'prep',
        ]

        for token in self.tokens:
            # if the token isn't a potential NP, skip it
            if token.dependency_type not in target_types:
                continue

            # now get the subtree
            subtree, root_ix = self._get_subtree(token.ix)

            # if the subtree contains a non-root `appos`, remove that
            subtree = self._remove_appos(subtree, root_ix)

            # in the case of an attr, check that the head is a noun
            if self._subtree_head_missing_required_noun(subtree, root_ix):
                continue

            # if the subtree is a single word, skip it
            # NOTE: makes sense to check this last as some of the other
            #       validation functions remove tokens
            if len(subtree) == 1:
                continue

            # if all validation checks pass, then we have a noun-phrase
            nps.append(subtree)

        # if we have a noun phrase that includes a prep, split the first half
        # as an additional NP
        split_prep_nps = []
        for np in nps:
            split_prep_nps += self._get_split_prep_nps(np)
        nps += split_prep_nps

        return nps

    @property
    def text(self) -> str:
        return ' '.join([str(x) for x in self.tokens])

    def serialize(self):
        return dill.dumps(self)


class Paragraph:

    def __init__(self, sentences: List[Sentence]):
        self.sentences = sentences

    def __len__(self):
        # number of tokens
        return sum(len(x) for x in self.sentences)

    def __repr__(self):
        return self.text

    @property
    def entities(self) -> List[Token]:
        entities = []
        for x in self.sentences:
            entities += x.entities
        return entities

    @property
    def text(self) -> str:
        return ' '.join([str(x) for x in self.sentences])

    @property
    def tokens(self) -> List[str]:
        tokens = []
        for s in self.sentences:
            tokens += s.tokens
        return tokens

    def serialize(self):
        return dill.dumps(self)


class Document:

    def __init__(self, paragraphs: List[Paragraph]):
        self.paragraphs = paragraphs

    def __len__(self):
        # number of tokens
        return sum(len(x) for x in self.paragraphs)

    def __repr__(self):
        return self.text

    @property
    def entities(self) -> List[Token]:
        entities = []
        for x in self.paragraphs:
            entities += x.entities
        return entities

    @property
    def text(self) -> str:
        return '\n\n'.join([str(x) for x in self.paragraphs])

    @property
    def tokens(self) -> List[str]:
        tokens = []
        for s in self.paragraphs:
            tokens += s.tokens
        return tokens

    def serialize(self):
        return dill.dumps(self)
