from typing import List, Optional
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
            uid: Optional[str] = None,
            dependency_head_uid: Optional[str] = None,
            dependency_type: Optional[str] = None
    ):
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.is_entity = is_entity
        self.entity_type = entity_type
        self.is_stop = is_stop
        self.uid = uid
        self.dependency_head_uid = dependency_head_uid
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

    @property
    def entities(self) -> List[Token]:
        return [x for x in self.tokens if x.is_entity]

    @property
    def noun_phrases(self) -> List[List[Token]]:
        # infer from the dependency parse
        raise NotImplementedError

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
