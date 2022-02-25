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
                    is_stop=self.is_stop if copy_meta_attrs else None,
                    ix=None,   # no way to do this without moving others so None
                    dependency_head_ix=self.dependency_head_ix if copy_meta_attrs else None,
                    dependency_type=self.dependency_type if copy_meta_attrs else None)
                for x in splits]
            return tokens
        else:
            return [self]

    def serialize(self):
        return dill.dumps(self)


def merge_tokens(
        tokens: List[Token],
        merge_det: bool = False,
        word_join_char: str = ' '
) -> List[Token]:
    """Merge tokens into one token.

    The main place this is used is merging phrases or entities.

    Args:
        tokens: List[Token].
        merge_det: Bool. Whether or not to merge determiners such as `the` or
          `a` into the resulting token.
        word_join_char: String. For English, for example, this is a space (the
          default value). For Mandarin, this should be ''.

    Returns:
        List[Token].
    """
    tokens_out = []

    # if the first token is a determiner, decide whether or not to separate it
    if tokens[0].pos == 'DET' and not merge_det:
        det = tokens[0]
        # make sure it is not marked as an entity
        det.is_entity = False
        det.entity_type = ''
        # append it to the tokens to return
        tokens_out.append(det)
        # remove it from the initial token list
        tokens.remove(det)

    # if there was only a determiner for some reason, return now
    if len(tokens) == 0:
        return tokens_out

    # with the remaining tokens, merge them based on the defined strategy
    root = get_root(tokens)
    merged = Token(
        # the text is simply joined on the join char
        text=word_join_char.join([x.text for x in tokens]),
        # a simple heuristic is to take the last POS, which is usually a NOUN
        # that is modified by the tokens to its left
        pos=tokens[-1].pos,
        # add the lemmas together
        lemma=word_join_char.join([x.lemma for x in tokens]),
        # again, use the last token as a heuristic
        is_entity=tokens[-1].is_entity,
        entity_type=tokens[-1].entity_type,
        # this is only a stop if all tokens are stops
        is_stop=all(x.is_stop for x in tokens),
        # this should be the root/head of the subsequence
        ix=root.ix,
        dependency_head_ix=root.dependency_head_ix,
        dependency_type=root.dependency_type)

    tokens_out.append(merged)

    return tokens_out


def get_root(subtree: List[Token]) -> Token:
    return next(
        x for x in subtree
        if x.dependency_head_ix not in [y.ix for y in subtree])


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

    @staticmethod
    def _drop_prep_subtree(np: List[Token], prep_ix: int) -> List[Token]:
        prep_root = next(x for x in np if x.ix == prep_ix)
        queue = [prep_root]
        while len(queue) > 0:
            children = [x for x in np if x.dependency_head_ix == prep_root.ix]
            for child in children:
                queue.append(child)
            np.remove(prep_root)
            queue.remove(prep_root)
            if len(queue) > 0:
                prep_root = queue[0]
        return np

    @staticmethod
    def _get_root_ix(subtree: List[Token]) -> int:
        root_ix = next(
            x.ix for x in subtree
            if x.dependency_head_ix not in [y.ix for y in subtree])
        return root_ix

    def _get_subtree(
            self,
            ix: int,
            tokens: List[Token]
    ) -> Tuple[List[Token], int]:
        root = next(x for x in tokens if x.ix == ix)
        subtree_root_ix = root.ix
        subtree = [root]
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
                appos_subtree, _ = self._get_subtree(x.ix, subtree)
                for y in appos_subtree:
                    # this check required as may already have been removed
                    if y in subtree:
                        subtree.remove(y)

        # finally, make sure the tokens are sorted correctly before returning
        return self._sort_tokens(subtree)

    @staticmethod
    def _remove_det(subtree: List[Token]) -> List[Token]:
        if subtree[0].dependency_type == 'det':
            return subtree[1:]
        return subtree

    def _split_prep_nps(
            self,
            np: List[Token]
    ) -> List[List[Token]]:
        root_ix = self._get_root_ix(np)
        prep_nps = []
        preps = [x for x in np if x.dependency_type == 'prep']
        # basically, just add the subtrees of parents for each prep, minus the
        # prep subtree
        for prep in preps:
            if prep.ix == root_ix:
                continue
            subtree, _ = self._get_subtree(prep.dependency_head_ix, np)
            subtree = self._drop_prep_subtree(subtree, prep.ix)
            prep_nps.append(subtree)
        return prep_nps

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

    def _fix_np(self, subtree: List[Token], det: bool) -> List[Token]:
        root_ix = self._get_root_ix(subtree)

        # if the subtree contains a non-root `appos`, remove that
        subtree = self._remove_appos(subtree, root_ix)

        if not det:
            subtree = self._remove_det(subtree)

        return subtree

    def _np_is_valid(self, subtree: List[Token]) -> bool:
        root_ix = self._get_root_ix(subtree)

        # in the case of an attr, check that the head is a noun
        if self._subtree_head_missing_required_noun(subtree, root_ix):
            return False

        # if the subtree is a single word, skip it
        # NOTE: makes sense to check this last as some of the other
        #       validation functions remove tokens
        if len(subtree) == 1:
            return False

        # otherwise it is valid
        return True

    @property
    def entities(self) -> List[Token]:
        return [x for x in self.tokens if x.is_entity]

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 20
    ) -> List[List[Token]]:
        # if det=True, determiners will be included, e.g. "a cat"
        nps = []

        # refer to README.md for details and examples
        target_types = [
            'nsubj', 'dobj', 'pobj', 'appos', 'attr', 'cop', 'nsubj',
            'nsubjpass', 'obj',
        ]

        for token in self.tokens:
            # if the token isn't a potential NP, skip it
            if token.dependency_type not in target_types:
                continue

            # now get the subtree
            subtree, root_ix = self._get_subtree(token.ix, self.tokens)

            # if too long, skip right away
            if len(subtree) > max_len:
                continue

            # apply any necessary fixes
            subtree = self._fix_np(subtree, det)

            # if all validation checks pass, then add the noun-phrase
            if self._np_is_valid(subtree):
                nps.append(subtree)

        # if we have a noun phrase that includes a prep, split the first half
        # as an additional NP
        split_prep_nps = []
        for np in nps:
            splits = self._split_prep_nps(np)
            for snp in splits:
                snp = self._fix_np(snp, det=det)
                if self._np_is_valid(snp):
                    nps.append(snp)
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

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 20
    ) -> List[List[Token]]:
        nps = []
        for sentence in self.sentences:
            nps += sentence.get_noun_phrases(det=det, max_len=max_len)
        return nps

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

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 20
    ) -> List[List[Token]]:
        nps = []
        for paragraph in self.paragraphs:
            nps += paragraph.get_noun_phrases(det=det, max_len=max_len)
        return nps

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
