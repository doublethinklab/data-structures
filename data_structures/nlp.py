import dill
from typing import Dict, List, Optional, Tuple

from data_structures import base


class NlpBase:

    def serialize(self):
        return dill.dumps(self)


class Token(NlpBase):

    def __init__(
            self,
            text: str,
            pos: Optional[str] = None,
            lemma: Optional[str] = None,
            is_entity: Optional[bool] = None,
            entity_type: Optional[str] = None,
            is_hashtag: Optional[bool] = None,
            is_mention: Optional[bool] = None,
            is_url: Optional[bool] = None,
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
        self.is_hashtag = is_hashtag
        self.is_mention = is_mention
        self.is_url = is_url
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
                    is_hashtag=self.is_hashtag if copy_meta_attrs else None,
                    is_stop=self.is_stop if copy_meta_attrs else None,
                    is_mention=self.is_mention if copy_meta_attrs else None,
                    is_url=self.is_url if copy_meta_attrs else None,
                    ix=None,   # no way to do this without moving others so None
                    dependency_head_ix=self.dependency_head_ix
                        if copy_meta_attrs else None,
                    dependency_type=self.dependency_type
                        if copy_meta_attrs else None)
                for x in splits]
            return tokens
        else:
            return [self]


class Sentence(NlpBase):

    def __init__(
            self,
            tokens: List[Token]
    ):
        self.tokens = tokens
        # one pass over the tokens to get required info for phrase extraction
        self.children, self.dep2ixs = get_tree_info(tokens)

    def __len__(self):
        # number of tokens
        return len(self.tokens)

    def __repr__(self):
        return self.text

    @property
    def entities(self) -> List[Token]:
        return [x for x in self.tokens if x.is_entity]

    @property
    def hashtags(self) -> List[Token]:
        return [x for x in self.tokens if x.is_hashtag]

    @property
    def mentions(self) -> List[Token]:
        return [x for x in self.tokens if x.is_mention]

    @property
    def urls(self) -> List[Token]:
        return [x for x in self.tokens if x.is_url]

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 10
    ) -> List[List[Token]]:
        # check to maintain backwards compatibility will dills
        if 'dep2ixs' not in self.__dict__:
            self.children, self.dep2ixs = get_tree_info(self.tokens)

        # refer to README.md for details and examples
        target_types = [
            'nsubj', 'dobj', 'pobj', 'appos', 'attr', 'cop', 'nsubjpass', 'obj',
        ]
        head_should_be_noun = ['cop', 'attr', 'dobj']

        np_ixs = []

        # use our map to lookup those ixs we need
        for dep in target_types:
            if dep in self.dep2ixs:
                for ix in self.dep2ixs[dep]:
                    # NOTE: the below should be refactored into a separate
                    # function

                    # noun check here
                    if dep in head_should_be_noun \
                            and self.tokens[ix].pos != 'NOUN':
                        continue
                    # if we somehow have a terminal node, continue now
                    if len(self.children[ix]) == 0:
                        continue
                    # don't take pronouns
                    if self.tokens[ix].pos == 'PRON':
                        continue
                    # now look for the span of the NP
                    # NOTE: this is probably the most expensive operation
                    left, right = get_left_right(self.children, ix)
                    # skip spans that are too long
                    if right - left > max_len:
                        continue
                    # if left is a PREP, increment
                    if self.tokens[left].dependency_type == 'prep':
                        left += 1
                    # if no tokens left, skip
                    if left > len(self.tokens) - 1:
                        continue
                    # if left is a det and we don't want it, increment
                    if self.tokens[left].dependency_type == 'det' and not det:
                        left += 1
                    # if no tokens left, skip
                    if left > len(self.tokens) - 1:
                        continue
                    # check if we are left with just one token
                    if right - left < 2:
                        continue
                    # if we get to here, we are good to go
                    np_ixs.append([left, right])

        # now we just look up the tokens with the ixs
        nps = [
            [self.tokens[i] for i in range(left, right + 1)]
            for left, right in np_ixs
        ]

        return nps

    def get_verb_phrases(
            self,
            max_len: int = 10
    ) -> List[List[Token]]:
        # check to maintain backwards compatibility will dills
        if 'dep2ixs' not in self.__dict__:
            self.children, self.dep2ixs = get_tree_info(self.tokens)

        # refer to README.md for details and examples
        target_types = [
            'advcl', 'ccomp', 'csubj', 'csubjpass', 'dobj', 'parataxis',
            'pcomp', 'relcl', 'rcmod', 'root', 'ROOT', 'xcomp',
        ]
        head_should_be_verb = ['dobj', 'root', 'ROOT']
        verb_pos = ['VERB', 'AUX']

        vp_ixs = []

        # use our map to lookup those ixs we need
        for dep in target_types:
            if dep in self.dep2ixs:
                for ix in self.dep2ixs[dep]:
                    # verb check here
                    if dep in head_should_be_verb \
                            and self.tokens[ix].pos not in verb_pos:
                        continue
                    # if we somehow have a terminal node, continue now
                    if len(self.children[ix]) == 0:
                        continue
                    # now look for the span of the NP
                    # NOTE: this is probably the most expensive operation
                    left, right = get_left_right(self.children, ix)
                    # skip spans that are too long
                    if right - left > max_len:
                        continue
                    # check if we are left with just one token
                    if right - left < 2:
                        continue
                    # if we get to here, we are good to go
                    vp_ixs.append([left, right])

        # now we just look up the tokens with the ixs
        vps = [
            [self.tokens[i] for i in range(left, right + 1)]
            for left, right in vp_ixs
        ]

        return vps

    @property
    def text(self) -> str:
        return ' '.join([str(x) for x in self.tokens])


class Paragraph(NlpBase):

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
    def hashtags(self) -> List[Token]:
        hashtags = []
        for x in self.sentences:
            hashtags += x.hashtags
        return hashtags

    @property
    def mentions(self) -> List[Token]:
        mentions = []
        for x in self.sentences:
            mentions += x.mentions
        return mentions

    @property
    def urls(self) -> List[Token]:
        urls = []
        for x in self.sentences:
            urls += x.urls
        return urls

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 10
    ) -> List[List[Token]]:
        nps = []
        for sentence in self.sentences:
            nps += sentence.get_noun_phrases(det=det, max_len=max_len)
        return nps

    def get_verb_phrases(self, max_len: int = 10) -> List[List[Token]]:
        vps = []
        for sentence in self.sentences:
            vps += sentence.get_verb_phrases(max_len=max_len)
        return vps

    @property
    def text(self) -> str:
        return ' '.join([str(x) for x in self.sentences])

    @property
    def tokens(self) -> List[str]:
        tokens = []
        for s in self.sentences:
            tokens += s.tokens
        return tokens


class Document(NlpBase):

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
    def hashtags(self) -> List[Token]:
        hashtags = []
        for x in self.paragraphs:
            hashtags += x.hashtags
        return hashtags

    @property
    def mentions(self) -> List[Token]:
        mentions = []
        for x in self.paragraphs:
            mentions += x.mentions
        return mentions

    @property
    def urls(self) -> List[Token]:
        urls = []
        for x in self.paragraphs:
            urls += x.urls
        return urls

    def get_noun_phrases(
            self,
            det: bool = False,
            max_len: int = 10
    ) -> List[List[Token]]:
        nps = []
        for paragraph in self.paragraphs:
            nps += paragraph.get_noun_phrases(det=det, max_len=max_len)
        return nps

    def get_verb_phrases(self, max_len: int = 10) -> List[List[Token]]:
        vps = []
        for paragraph in self.paragraphs:
            vps += paragraph.get_verb_phrases(max_len=max_len)
        return vps

    @property
    def sentences(self) -> List[Sentence]:
        sentences = []
        for paragraph in self.paragraphs:
            sentences += paragraph.sentences
        return sentences

    @property
    def text(self) -> str:
        return '\n\n'.join([str(x) for x in self.paragraphs])

    @property
    def tokens(self) -> List[str]:
        tokens = []
        for s in self.paragraphs:
            tokens += s.tokens
        return tokens


#
# functions
#


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
        del tokens[0]

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
        #
        is_hashtag=all(t.is_hashtag for t in tokens),
        is_mention=all(t.is_mention for t in tokens),
        is_url=all(t.is_url for t in tokens),
        # this is only a stop if all tokens are stops
        is_stop=all(x.is_stop for x in tokens),
        # this should be the root/head of the subsequence
        ix=root.ix,
        dependency_head_ix=root.dependency_head_ix,
        dependency_type=root.dependency_type)

    tokens_out.append(merged)

    return tokens_out


def get_root(subtree: List[Token]) -> Token:
    root = next(
        (x for x in subtree
         if x.dependency_head_ix not in [y.ix for y in subtree]),
        None)
    # debugging while we improve this code
    if not root:
        print([x.text for x in subtree])
        print([x.ix for x in subtree])
        print([x.dependency_head_ix for x in subtree])
        raise Exception
    return root


def get_tree_info(
        tokens: List[Token]
) -> Tuple[Dict[int, List[int]], Dict[str, List[int]]]:
    ix2list = {x.ix: ix for ix, x in enumerate(tokens)}
    children = {ix: [] for ix in range(len(tokens))}
    dep2ixs = {}
    for token in tokens:
        token_ix = ix2list[token.ix]
        if token.dependency_head_ix and token.dependency_head_ix in ix2list:
            head_ix = ix2list[token.dependency_head_ix]
            children[head_ix].append(token_ix)
        if token.dependency_type not in dep2ixs:
            dep2ixs[token.dependency_type] = []
        dep2ixs[token.dependency_type].append(token_ix)
    return children, dep2ixs


def get_left_right(children: Dict, ix: int) -> Tuple[int, int]:
    if len(children[ix]) == 0:
        raise ValueError
    queue = [ix]
    all_children = []
    while len(queue) > 0:
        current_head = queue[0]
        current_children = children[current_head]
        all_children += current_children
        queue += current_children
        del queue[0]
    return min(all_children), max(all_children)
