from timeit import default_timer as timer
import vlibras_translate

def timeit(method):
    def timed(*args, **kw):
        ts = timer()
        result = method(*args, **kw)
        te = timer()
        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed

@timeit
def process(tr, gr, gi, **kw):
    return tr.preprocess_specialist(gr, gi, **kw)

if __name__ == '__main__':
    tr = vlibras_translate.translation.Translation(verbose=0)

    try:
        out = process(tr, 'ESTAR POUCO BÊBADO [PONTO]', 'FUDER (--)BEBER [PONTO]', intensifier_on_right=False)
        print(out, end='\n\n')
        out = process(tr, 'ESTAR POUCO BÊBADO [PONTO]', 'fuder BEBER(--) [PONTO]')
        print(out, end='\n\n')

        out = process(tr, 'ESTAR POUCO BÊBADO [PONTO]', '1S_BEBER_3P [PONTO]')
        print(out, end='\n\n')

        out = process(tr, 'ESTAR POUCO BÊBADO [PONTO]', 'BALÃO_REDONDO&HISTÓRIA_QUADRINHO [PONTO]')
        print(out, end='\n\n')

        out = process(tr, 'ESTAR POUCO BÊBADO [PONTO]', 'DIRETOR_GERAL [PONTO]')
        print(out, end='\n\n')

    except KeyboardInterrupt:
        quit()
