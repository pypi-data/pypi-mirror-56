import time
#import psutil
import sys

from .cogroo4py.cogroo4py import Cogroo
#from os import path
#from subprocess import PIPE, Popen
from interruptingcow import timeout


def lemmatize_cogroo_check(time, word):
    try:
        with timeout(time, exception=RuntimeError):
            cogroo = Cogroo.instance()
            word_lemma = cogroo.lemmatize(word)
            if not word_lemma:
                raise Exception
            print('0')
            sys.exit(0)
            pass
    except Exception:
        print('1')
        sys.exit(1)


if __name__ == "__main__":
    lemmatize_cogroo_check(10, "teste")
