#---------------------------------
#
# Author: Caio Moraes
# Email: <caiomoraes.cesar@gmail.com>
# GitHub: MoraesCaio
#
# LAViD - Laboratório de Aplicações de Vídeo Digital
#
#---------------------------------

import re
from unidecode import unidecode
from .number import Number

class Postprocessor():

    def __init__(self):
        self._number = Number()

    def converter_extenso(self, sentence):
        '''Convert spelled out numbers back to digits.'''
        tokens = [[unidecode(x.lower()), ''] for x in sentence.split()]

        for token in tokens:
            if token[0] == 'uma':
                token[1] = 'D-UM-F'
            elif token[0] == 'umas':
                token[1] = 'D-UM-F-P'
            elif token[0] == 'um':
                token[1] = 'D-UM'
            elif token[0] == 'uns':
                token[1] = 'D-UM-P'
            elif token[0] == 'duas':
                token[1] = 'NUM-F'
            elif token[0] in Number.acceptable:
                token[1] = 'NUM'
            elif token[0] == 'e':
                token[1] = 'CONJ'
            else:
                token[1] = ''

        return ' '.join([x[0].upper() for x in self._number.converter_extenso(tokens) if not x[0] == 'e'])

    def convert_directionals(self, sentence):
        '''Convert PERGUNTAR_1S_3S -> 1S_PERGUNTAR_3S.'''
        return re.sub(r'(\w+)_([123][SP])(_[123][SP])', r'\2_\1\3', sentence)

    def postprocess(self, sentence):
        '''Run all postprocessing methods in sequence and return final sentence.'''
        sentence = self.convert_directionals(sentence)
        sentence = self.converter_extenso(sentence)

        return sentence