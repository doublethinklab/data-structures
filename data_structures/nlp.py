from typing import List, Optional


class Token:

    def __init__(self,
                 text: str,
                 pos: Optional[str] = None,
                 lemma: Optional[str] = None,
                 is_entity: Optional[bool] = None,
                 entity_type: Optional[str] = None,
                 is_stop: Optional[bool] = None):
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.is_entity = is_entity
        self.entity_type = entity_type
        self.is_stop = is_stop

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return self.text


class Sentence:

    def __init__(self, tokens: List[Token]):
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
    def text(self) -> str:
        return ' '.join([str(x) for x in self.tokens])


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
