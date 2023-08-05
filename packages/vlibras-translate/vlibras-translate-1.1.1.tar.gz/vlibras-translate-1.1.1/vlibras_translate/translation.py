#---------------------------------
#
# Author: Caio Moraes
# Email: <caiomoraes.cesar@gmail.com>
# GitHub: MoraesCaio
#
# LAViD - Laboratório de Aplicações de Vídeo Digital
#
#---------------------------------

from .aelius_tagger import ClassificaSentencas
from .name_checking import NameChecking
from .lemma import Lemma
from .char_preprocessing import CharPreprocessing
from .number import Number
from .word_processing import WordProcessing
from .utils import now
import argparse
from copy import deepcopy
import re


class Translation():

    name_symbol = '"'
    number_symbol = '\''
    error_symbol = '#'
    verbose = 0

    def __init__(self, verbose=0):

        self.char_prep = CharPreprocessing()
        self.classifier = ClassificaSentencas()
        self.lemmatizer = Lemma(verbose)
        self.number = Number()
        self.word_processing = WordProcessing()
        self.dl = None

        # OUTPUTS
        self.pp_pt_train = ''
        self.pp_glosa_train = ''
        self.pp_pt_test = ''
        self.rbmt_glosa = ''
        self.nmt_glosa = ''
        self.verbose = verbose

    def first_steps(self, phrase, glosa=False, do_tagging=True, intensifier_on_right=True):

        # remove useless chars and some applying some preprocessing for numbers
        phrase = self.char_prep.preprocess(phrase, glosa=glosa)

        try:
            tagged = self.classifier.iniciar_classificacao(phrase, glosa=glosa, do_tagging=do_tagging, intensifier_on_right=intensifier_on_right)
        except:
            raise ValueError('Sentence contains non-latin-1 characters:\n' + phrase)

        # redução de tags de números por extenso para cardinais
        tagged = self.number.simplificar_sentenca(tagged)
        # pontos decimais são substituídos por vírgulas
        tagged = self.char_prep.set_number_decimal_to_commas(tagged)
        # caixa baixa
        tagged = [[tag[0].lower(), tag[1]] for tag in tagged]

        return tagged

    def rule_translation(self, phrase):

        tagged = self.first_steps(phrase)

        # SUBSTITUIÇÃO POR SÍMBOLOS
        # se é arquivo de teste, NÃO substitui NOMES, NÚMEROS e ERROS ORTOGRÁFICAOS por símbolos
        tagged = self.word_processing.mask_tag_sentence(tagged, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)

        # tags
        if self.verbose > 1:
            print(f'{[now()]} tagged (train):', tagged)

        rbmt_glosa = self.glosa_final_steps(tagged)
        rbmt_glosa = self.word_processing.restore_named_entities(rbmt_glosa, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)
        rbmt_glosa = self.word_processing.replace_synonyms(rbmt_glosa)

        if self.verbose > 0:
            print(f'\nGLOSA (RBMT):\n{rbmt_glosa}\n')

        return rbmt_glosa

    def rule_translation_for_dl(self, phrase):
        '''Versão alterada da função rule_translation para uso com o módulo de deep learning.
        '''
        if not self.dl:
            try:
                from vlibras_deeplearning import deep_translation
                self.dl = deep_translation.DeepTranslation()
            except ImportError:
                print('The `vlibras-deeplearning` python package must be installed to use this functionality.')
                return

        tagged = self.first_steps(phrase)

        # TODO: substituir as chamadas de `mask_tag_sentence` e `restore_named_entities` pelas novas funções
        tagged = self.word_processing.mask_tag_sentence(tagged, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)

        if self.verbose > 1:
            print(f'{[now()]} tagged (test):', tagged)

        rbmt_glosa = self.glosa_final_steps(tagged)
        rbmt_glosa = self.word_processing.restore_named_entities(rbmt_glosa, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)
        nmt_glosa = self.dl.deep_translation(rbmt_glosa)
        nmt_glosa = self.word_processing.replace_synonyms(nmt_glosa)

        if self.verbose > 0:
            print(f'\nGLOSA (NMT):\n{nmt_glosa}\n')

        return nmt_glosa

    def preprocess_pt(self, phrase):

        tagged = self.first_steps(phrase)

        # tags
        if self.verbose > 1:
            print(f'{[now()]} tagged (test):', tagged)

        # test file
        pp_pt_test = self.pt_final_steps(tagged)

        if self.verbose > 0:
            print(f'\nPreprocessed PT:\n{pp_pt_test}\n')

        return pp_pt_test

    def preprocess_train_files(self, phrase):

        tagged = self.first_steps(phrase)

        # SUBSTITUIÇÃO POR SÍMBOLOS
        # se é arquivo de teste, NÃO substitui NOMES, NÚMEROS e ERROS ORTOGRÁFICAOS por símbolos
        tagged = self.word_processing.mask_tag_sentence_pt_glosa(tagged, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)

        # tags
        if self.verbose > 1:
            print(f'{[now()]} tagged (train):', tagged)

        # train files
        pp_pt_train = self.pt_final_steps(tagged)
        pp_pt_train = self.char_prep.summarize_train_file(pp_pt_train)

        glosa_tagged = deepcopy(tagged)
        pp_glosa_train = self.glosa_final_steps(glosa_tagged)
        pp_glosa_train = self.char_prep.summarize_train_file(pp_glosa_train)

        if self.verbose > 0:
            print(f'\nTrain PT:\n{pp_pt_train}\n')
            print(f'Train GLOSA:\n{pp_glosa_train}\n')

        return pp_pt_train, pp_glosa_train

    def preprocess_specialist(self, glosa_rule, glosa_interp, intensifier_on_right=True):
        tokenized_gr = self.first_steps(glosa_rule.lower(), glosa=True, do_tagging=False, intensifier_on_right=intensifier_on_right)
        tokenized_gi = self.first_steps(glosa_interp.lower(), glosa=True, do_tagging=False, intensifier_on_right=intensifier_on_right)

        if self.verbose > 0:
            print('tokenized_gr', tokenized_gr)
            print('tokenized_gi', tokenized_gi)

        masked_gr, masked_gi = self.word_processing.mask_tag_sentence_gr_gi(tokenized_gr, tokenized_gi, name_symbol=self.name_symbol, number_symbol=self.number_symbol, error_symbol=self.error_symbol)

        masked_gr = self.glosa_final_steps(masked_gr, already_lemmatized=True)
        masked_gr = self.char_prep.summarize_train_file(masked_gr)

        masked_gi = self.glosa_final_steps(masked_gi, already_lemmatized=True)
        masked_gi = self.char_prep.summarize_train_file(masked_gi)

        if self.verbose > 0:
            print(f'masked_gr:\n{masked_gr}')
            print(f'masked_gi:\n{masked_gi}')

        return masked_gr, masked_gi

    def pt_final_steps(self, tagged):
        # concatena sentença e desfazendo parsing de [ponto], [exclamação] e [interrogação]
        pt_sentence = ' '.join(tag[0] for tag in tagged)
        pt_sentence = self.char_prep.restore_punctuation(pt_sentence)

        return pt_sentence

    def glosa_final_steps(self, tagged, already_lemmatized=False):

        # substitui o símbolo de vírgula pela palavra 'vírgula' (apenas para números)
        tagged = self.char_prep.set_number_decimal_to_token(tagged)

        # palavras da lista branca não são lematizadas
        tagged = self.word_processing.mask_whitelist_words(tagged)

        # TODO modify remove_mes...() to move the pronoun and move it to a point before Aelius' classification
        tagged = [[self.char_prep.remove_mesoclise_enclise(tag[0]), tag[1]] for tag in tagged]

        # lematiza, concatena sentença e apaga excesso de espaços
        if not already_lemmatized:
            tagged = [[self.lemmatizer.lemmatize_aelius_tag(t)[0], t[1]] for t in tagged]

        glosa_sentence = ' '.join([t[0] for t in tagged])
        glosa_sentence = self.char_prep.remove_multiple_spaces(glosa_sentence)

        # desfaz o mascaramento da lista branca
        glosa_sentence = self.word_processing.restore_whitelist_words(glosa_sentence)

        glosa_sentence = re.sub(r'(?<![\(-])-(?!=[-\)])', '_', glosa_sentence)
        glosa_sentence = glosa_sentence.upper()

        return glosa_sentence


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('phrase', help='Phrase')
    parser.add_argument('-i', '--interpreter', help='interpreter phrase.')
    parser.add_argument('-s', '--specialist', help='Preprocess specialist phrase.')
    parser.add_argument('-t', '--train-files', action='store_true', help='Preprocessing for train files.')
    parser.add_argument('-p', '--preprocess-pt', action='store_true', help='Preprocessing for test file.')
    parser.add_argument('-r', '--rbmt-glosa', action='store_true', help='RBMT GLOSA.')
    parser.add_argument('-n', '--nmt-glosa', action='store_true', help='NMT GLOSA.')
    parser.add_argument('-v', '--verbose', default=1, action='count', help='Verbose.')

    args, _ = parser.parse_known_args()

    translation = Translation(verbose=args.verbose)

    if args.rbmt_glosa:
        translation.rule_translation(args.phrase)
    elif args.nmt_glosa:
        translation.rule_translation_for_dl(args.phrase)
    elif args.train_files:
        if args.interpreter:
            translation.preprocess_specialist(args.phrase, args.interpreter)
        else:
            translation.preprocess_train_files(args.phrase)
    elif args.preprocess_pt:
        translation.preprocess_pt(args.phrase)
    elif args.specialist:
        translation.preprocess_specialist(args.phrase, args.specialist)


if __name__ == '__main__':
    main()
