# -*- coding: utf-8 -*-
"""
Based on letrustech's fork of gpassero's original cogroo4py.

Improvements over gpassero's version (by contemmcm):
    * Better UTF-8 support
    * Added unit tests

Improvements over letrustech's version (by samueldemoura):
    * Migrate to Python 3
    * Replace py4j with pyjnius to solve intermittent timeout issue
"""
import logging
import os
import re

os.environ['CLASSPATH'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'cogroo4py.jar'
)
if not 'JAVA_HOME' in os.environ:
    # TODO: replace this with a call to `readlink -f javac` and get path from there
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
from jnius import autoclass

LOGGER = logging.getLogger(__name__)


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    MSG_CALL_INSTANCE = 'Singletons must be accessed through `instance()`.'

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError(self.MSG_CALL_INSTANCE)

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def find(pattern, text):
    return [(i.start(), i.end()) for i in re.finditer(pattern, text)]


class Token:
    def __init__(self, cogroo_token):
        self.lemmas = list(cogroo_token.getLemmas())
        self.lexeme = cogroo_token.getLexeme()

        if self.lemmas:
            self.lemma = self.lemmas[0]
        else:
            self.lemma = self.lexeme

        self.lemma = self.lemma.replace('_', ' ')
        self.chunk = cogroo_token.getChunkTag()
        self.chunk_head = cogroo_token.isChunkHead()
        self.synchunk = cogroo_token.getSyntacticTag()
        self.pos = cogroo_token.getPOSTag()
        self.feat = cogroo_token.getFeatures()
        self.start = cogroo_token.getStart()
        self.end = cogroo_token.getEnd()
# TODO analyze when number to string conversion may be useful
#        if self.pos == 'num' and re.match('\d+[.,]?\d*', self.lemma):
#            try:
#                num = float(self.lemma.replace(',', '.'))
#                self.lemma = num2words(num, lang='pt_BR')
#            except:
#                print('Couldn\'t convert ' + self.lemma + ' to number.')

    def __repr__(self):
        return '{0}#{1} {2}'.format(self.lexeme, self.pos, self.feat) # .encode('utf8')


class Chunk:
    def __init__(self, sentence, cogroo_chunk):
        self.tag = cogroo_chunk.getTag()
        tokens = cogroo_chunk.getTokens()
        if tokens:
            self.start = tokens.get(0).getStart()
            self.end = tokens.get(tokens.size() - 1).getEnd()
            self.tokens = []
            for token in sentence.tokens:
                if token.start >= self.start and token.end <= self.end:
                    self.tokens.append(token)

                elif token.end > self.end:
                    break

    def __repr__(self):
        return '{0}[{1}]'.format(self.tag, self.tokens)


class Sentence:
    def __init__(self, cogroo_sentence, paragraph):
        self.text = cogroo_sentence.getText()
        self.start = cogroo_sentence.getStart()
        self.end = cogroo_sentence.getEnd()
        self.paragraph = paragraph

        self.tokens = []
        token_it = cogroo_sentence.getTokens().iterator()
        while token_it.hasNext():
            token = token_it.next()
            self.tokens.append(Token(token))

        self.chunks = []
        chunk_it = cogroo_sentence.getChunks().iterator()
        while chunk_it.hasNext():
            chunk = chunk_it.next()
            self.chunks.append(Chunk(self, chunk))

        self.synchunks = []
        synchunk_it = cogroo_sentence.getSyntacticChunks().iterator()
        while synchunk_it.hasNext():
            synchunk = synchunk_it.next()
            self.synchunks.append(Chunk(self, synchunk))

    def __repr__(self):
        return self.text # .encode('utf8')


class Document:
    def __init__(self, cogroo_doc):
        self.text = cogroo_doc.getText()

        paragraphs_ind = find('\n', cogroo_doc.getText())
        paragraph = 1
        last_sent_end = -1

        self.sentences = []
        sentence_it = cogroo_doc.getSentences().iterator()
        while sentence_it.hasNext():
            sentence = sentence_it.next()
            if paragraphs_ind:
                start = paragraphs_ind[0][0]
                if start <= last_sent_end and last_sent_end != -1:
                    del paragraphs_ind[0]
                    paragraph += 1

            self.sentences.append(Sentence(sentence, paragraph))
            last_sent_end = sentence.getEnd()

        self.paragraphs = []
        for sentence in self.sentences:
            p = sentence.paragraph
            if len(self.paragraphs) < p:
                self.paragraphs.append([])

            self.paragraphs[-1].append(sentence)

        # TODO: fix this. can't use getClass with pyjnius' autoclass
        if True: #cogroo_doc.getClass().getSimpleName() == 'CheckDocument':
            self.mistakes = []

            try:
                mistake_it = cogroo_doc.getMistakes().iterator()
                while mistake_it.hasNext():
                    cogroo_mistake = mistake_it.next()
                    self.mistakes.append(Mistake(cogroo_mistake))
            except AttributeError:
                # couldn't call getMistakes(), which means this isn't an
                # instance of CheckDocument. ignore.
                pass

    def __repr__(self):
        return self.text # .encode('utf8')


class Mistake:

    def __init__(self, cogroo_mistake):
        self.rule_id = cogroo_mistake.getRuleIdentifier()
        self.short_msg = cogroo_mistake.getShortMessage()
        self.long_msg = cogroo_mistake.getLongMessage()
        self.full_msg = cogroo_mistake.getFullMessage()
        suggestions = cogroo_mistake.getSuggestions()
        self.suggestions = [s for s in suggestions]
        self.start = cogroo_mistake.getStart()
        self.end = cogroo_mistake.getEnd()
        self.context = cogroo_mistake.getContext()
        self.rule_priority = cogroo_mistake.getRulePriority()

    def __repr__(self):
        return '[{0}] {1}'.format(self.rule_id, self.short_msg) # .encode('utf8')


@Singleton
class Cogroo:

    def __init__(self):
        self.javacls = autoclass('br.edu.univali.lia.cogroo.CogrooPythonInterface')
        self.analyzer = self.javacls()
        self.pos_tags = self._pos_tags()
        self.feat_tags = self._feat_tags()
        self.chunk_tags = self._chunk_tags()
        self.synchunk_tags = self._synchunk_tags()

    def analyze(self, text):
        try:
            doc = self.analyzer.analyze(text)
        # pylint: disable = broad-except
        except Exception:
            # TODO: check this workaround for better solution
            text = re.sub(', e a', ', E a', text)
            doc = self.analyzer.analyze(text)

        return Document(doc)

    def _safe_analyse(self, text):
        if text is None or text == '':
            return None

        if not isinstance(text, Document):
            return self.analyze(text)
        return text

    def grammar_check(self, text):
        return Document(self.analyzer.grammarCheck(text))

    def lemmatize(self, text):
        doc = self._safe_analyse(text)

        if doc is None:
            return ''

        last_paragraph = -1
        ret = []
        for sentence in doc.sentences:
            if sentence.paragraph > last_paragraph and last_paragraph != -1:
                ret.append('\n')

            for token in sentence.tokens:
                ret.append(token.lemma)

            last_paragraph = sentence.paragraph

        return ' '.join(ret)

    def pos_tag(self, text):
        doc = self._safe_analyse(text)

        if doc is None:
            return ''

        ret = []
        for sentence in doc.sentences:
            for token in sentence.tokens:
                ret.append(token.lexeme + '#' + token.pos)

        return ' '.join(ret)

    def chunk_tag(self, text, type_='normal'):
        doc = self._safe_analyse(text)

        if doc is None:
            return ''

        ret = []
        for sentence in doc.sentences:
            if type_ == 'normal':
                chunks = sentence.chunks
            else:
                chunks = sentence.synchunks

            for chunk in chunks:
                tokens = []
                for token in chunk.tokens:
                    tokens.append(token.lexeme)

                ret.append(chunk.tag + '[' + ' '.join(tokens) + ']')

        return ' '.join(ret)

    def _pos_tags(self):
        pos = {}
        pos.update({"n": "substantivo"})
        pos.update({"prop": "nome próprio"})
        pos.update({"art": "artigo"})
        pos.update({"pron": "pronome"})
        pos.update({"pron-pers": "pronome pessoal"})
        pos.update({"pron-det": "pronome determinativo"})
        pos.update({"pron-indp": "substantivo/pron-indp"})
        pos.update({"adj": "adjetivo"})
        pos.update({"n-adj": "substantivo/adjetivo"})
        pos.update({"v": "verbo"})
        pos.update({"v-fin": "verbo finitivo"})
        pos.update({"v-inf": "verbo infinitivo"})
        pos.update({"v-pcp": "verbo particípio"})
        pos.update({"v-ger": "verbo gerúndio"})
        pos.update({"num": "numeral"})
        pos.update({"prp": "preposição"})
        pos.update({"adj": "adjetivo"})
        pos.update({"conj": "conjunção"})
        pos.update({"conj-s": "conjunção subordinativa"})
        pos.update({"conj-c": "conjunção coordenativa"})
        pos.update({"intj": "interjeição"})
        pos.update({"adv": "advérbio"})
        pos.update({"xxx": "outro"})
        return pos

    def _feat_tags(self):
        feat = {}

        feat.update({"M": "masculino"})
        feat.update({"F": "feminino"})
        feat.update({"M/F": "masculino/feminino"})

        feat.update({"S": "singular"})
        feat.update({"P": "plural"})

        feat.update({"NOM": "nominativo"})
        feat.update({"ACC": "acusativo"})
        feat.update({"DAT": "dativo"})
        feat.update({"PIV": "prepositivo"})

        feat.update({"1": "primeira pessoa"})
        feat.update({"2": "segunda pessoa"})
        feat.update({"3": "terceira pessoa"})

        feat.update({"1S": "primeira pessoa singular"})
        feat.update({"2S": "segunda pessoa singular"})
        feat.update({"3S": "terceira pessoa singular"})
        feat.update({"1P": "primeira pessoa plural"})
        feat.update({"2P": "segunda pessoa plural"})
        feat.update({"3P": "terceira pessoa plural"})

        feat.update({"PR": "presente"})
        feat.update({"IMPF": "imperfeito"})
        feat.update({"PS": "perfeito simples"})
        feat.update({"MQP": "mais-que-perfeito"})
        feat.update({"FUT": "futuro"})
        feat.update({"COND": "condicional"})

        feat.update({"IND": "indicativo"})
        feat.update({"SUBJ": "subjuntivo"})
        feat.update({"IMP": "imperativo"})

        feat.update({"xxx": "outro"})

        return feat

    def _chunk_tags(self):
        chunk = {}
        chunk.update({"NP": "nominal"})
        chunk.update({"VP": "verbal"})
        chunk.update({"PP": "preposicional"})
        chunk.update({"ADVP": "adverbial"})
        chunk.update({"xxx": "outro"})
        return chunk

    def _synchunk_tags(self):
        synchunk = {}
        synchunk.update({"ACC": "objeto direto"})
        synchunk.update({"ADVL": "adjunto adverbial"})
        synchunk.update({"APP": "aposição"})
        synchunk.update({"DAT": "objeto indireto pronominal"})
        synchunk.update({"OC": "predicativo do objeto"})
        synchunk.update({"P": "predicado"})
        synchunk.update({"PIV": "objeto preposicional"})
        synchunk.update({"SA": "complemento adverbial"})
        synchunk.update({"SC": "predicativo do sujeito"})
        synchunk.update({"SUBJ": "sujeito"})
        synchunk.update({"xxx": "outro"})
        return synchunk


cogroo = Cogroo.instance()
