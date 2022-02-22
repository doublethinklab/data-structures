# Data Structures

## NLP

### Dependency Parsing

#### SpaCy

```python
import spacy

# lists all symbols, deps are at the end of list in lowercase
symbols = dir(spacy.symbols)
# set this to the correct value to make the code below work
# there are 56 items in the list below
start_ix = -56
# prints the list shown next in this readme file
for s in symbols[start_ix:]:
    print(f'{s}: {spacy.explain(s)}')
```

[This resource](https://downloads.cs.stanford.edu/nlp/software/dependencies_manual.pdf)
is useful to understand the below.

- `acl`: clausal modifier of noun (adjectival clause). **Cannot find an example**.
- `acomp`: adjectival complement. "She looks {acomp very beautiful}."
- `advcl`: adverbial clause modifier. "If you know it, {advcl you should tell the teacher}."
- `advmod`: adverbial modifier. "{advmod Genetically} modified food".
- `agent`: agent. "The man has been killed {agent by {pobj the police}}."
- `amod`: adjectival modifier. "Sam eats {amod red} meat."
- `appos`: appositional modifier. "Sam, {appos my brother}, arrived."
- `attr`: attribute. "Bill is {attr an honest man}."
- `aux`: auxiliary. "Regan {aux has} died."
- `auxpass`: auxiliary (passive). "Kennedy has {auxpass been} killed."
- `cc`: coordinating conjunction. "Bill is big {cc->big and} honest."
- `ccomp`: clausal complement. "He says that {ccomp you like to swim}."
- `complm`: complementizer. **Cannot find an example**.
- `conj`: conjunct. "Bill is big and {conj->big honest}." Note the difference
  with the `cc` above is that the `and` does the coordinating, but the conjunction
  is in fact between big and honest. That what this captures.
- `cop`: copula. Example in the UD manual is "Bill is {cop an honest man}." 
  But the large English SpaCy model makes that relation come out as `acomp`.
- `csubj`: clausal subject. "{csubj To eat McDonald's} defies reason."
- `csubjpass`: clausal subject (passive). "{csubjpass That she lied} was suspected by everybody."
- `dep`: unclassified dependent.
- `det`: determiner.
- `dobj`: direct object.
- `expl`: expletive. "{expl->is There} is a ghost in the room."
- `hmod`: modifier in hyphenation. **Cannot find an example**.
- `hyph`: hyphen.
- `infmod`: infinitival modifier. According to the UD document, this has been 
  generalized as a case of `vmod` (not in this schema). "I don't have anything 
  {vmod->have to say} to you." However, SpaCy parses this as {relcl->anything say}.
- `intj`: interjection.
- `iobj`: indirect object. UD gives the example: "She gave {iobj->gave me} a raise."
  However, SpaCy parses this as a `dative`, which is curiously not in the schema
  here. The UD doc appears to suggest that `dative` is a synonym for `iobj`.
- `it`: None. **Cannot find an example**. Unless this really is just "it."
- `mark`: marker. "She says {mark->like that} you like to swim."
- `meta`: meta modifier. **Cannot find an example**.
- `neg`: negation modifier.
- `nmod`: modifier of nominal. 
- `nn`: noun compound modifier. The UD example is "{nn->futures Oil} {nn->futures price} futures."
  But the SpaCy model parses these two relations as `compound`, which is not in
  this schema.
- `npadvmod`: noun phrase as adverbial modifier. "{npadvmod->long 6 feet} long."
- `nsubj`: nominal subject. "{nsubj->defeated Clinton} defeated Dole."
- `nsubjpass`: nominal subject (passive). "{nsubjpass-> deafeated Dole} was defeated by Clinton."
- `num`: number modifier. "Sam ate {num 3} sheep."
- `number`: number compound modifier. "I have {number->thousand four} thousand sheep."
- `obj`: object. UD has the example: "She gave me a {obj->gave raise}." But the
  SpaCy model parses this as a `dobj`.
- `obl`: oblique nominal. UD has the example "Give the toys to the {obl->give children}."
  But the SpaCy model parses that relation as a `pobj` connect to `to`.
- `oprd`: object predicate. **Cannot find an example.**
- `parataxis`: parataxis. "The guy, Jon {parataxis->left said}, left early in the morning."
- `partmod`: participal modifier. UD has this generalized as a case of `vmod`.
  See `infmod` above.
- `pcomp`: complement of preposition. "We have no information on whether 
  {pcomp->on users} are at risk."
- `pobj`: object of preposition. "I sat on the {pobj->on chair}."
- `poss`: possession modifier. "{poss->offices their} offices".
- `possessive`: possessive modifier. "Bill'{possessive->Bill s} clothes". Except
  the SpaCy model parses this as `case`, which does not appear in the schema.
- `preconj`: pre-correlative conjunction. "{preconj->boys Both} the boys and girls are here."
- `prep`: prepositional modifier. "I saw a cat {prep->cat in} a hat."
- `prt`: particle. "They shut {part->shut down} the station."
- `punct`: punctuation.
- `quantmod`: modifier of quantifier. "{quantmod->200 About} 200 people came."
- `rcmod`: relative clause modifier. The UD example is "I saw the man you {rcmod->man} love."
  However, the SpaCy model parses this as a `relcl`.
- `relcl`: relative clause modifier. A SpaCy example: "Points to 
  {relcl->Points establish} are the following."
- `root`: root. 
- `sort_nums`: None.
- `xcomp`: open clausal complement. "He says that you like to {xcomp->like swim}."

Note, to visualize a parse in a jupyter notebook:

```python
import spacy
nlp = spacy.load('en_core_web_lg')
text = 'I saw a cat in a hat'
doc = nlp(text)
spacy.displacy.render(doc, style="dep")
```

Notes for extracting `NP`s:
- A `nsubj` and a `dobj` are good candidates, however:
- If a subtree consists of a single token that is a `PRON` we will want to skip:
  e.g., "{nsubj:PRON I} gave {dobj:PRON it} to him"
- Note that an `appos` should be removed from a `NP` that includes an `appos` 
  in its subtree (but note that an `appos` is itself a `NP`). For "Sam, my brother"
  we want "Sam" and "my brother" but not "Sam, my brother."
- An `agent` is not a `NP`, but the `pobj` attached to it is: 
  "The man has been killed {agent by {pobj the police}}."
- An `appos` is a `NP`: "Sam, {appos my brother}, arrived."
- An `attr` can be an `NP`: "Bill is {attr an honest man}." We may want to check
  that the head is a `NOUN`.
- A `cop` in theory can be a `NP`: UD manual has: "Bill is {cop an honest man}." 
  Although the SpaCy model makes that come out as an `attr`. This suggests that 
  we can look at a `cop` and check if the head is a `NOUN`.
- A `dobj` can be a `NP` or a `VP`. It seems that if the head of the `dobj` is
  a `VERB` or `AUX`, then it is a `VP`, else it is a `NP`.
- An `nsubj` is a `NP`.
- An `nsubjpass` is a `NP`.
- An `obj`, if it shows up, should be a `NP`.
- A `pobj` should be an `NP`.
- If we have a `prep` in a subtree, we should take another `NP` that consists of
  the `NP` preceding the `prep`. That which follows should be picked up by
  including the `pobj`. But the former wouldn't appear to be by the rules given
  above.

Notes for extracting `VP`s:
- An `advcl` should be a `VP`: "If you know it, {advcl you should tell the teacher}."
- A `ccomp` should be a `VP`: "He says that {ccomp you like to swim}."
- A `csubj` should be a `VP`: "{csubj To eat McDonald's} defies reason."
- A `csubjpass` may be a `VP`: "{csubjpass That she lied} was suspected by everybody."
- A `dobj` can be a `NP` or a `VP`. It seems that if the head of the `dobj` is
  a `VERB` or `AUX`, then it is a `VP`, else it is a `NP`.
- `parataxis` looks like a `VP`.
- Removing the `mark` from a subtree would result in a cleaner `VP`.
- A `pcomp` (without a `mark`) is a `VP`.
- A `relcl` or `rcmod` will be a `VP`.
- Normally the `root` will be a `VERB` or `AUX` and will be a `VP`.
- An `xcomp` will be a `VP`.
