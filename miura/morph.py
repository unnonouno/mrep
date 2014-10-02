import re
import subprocess

import MeCab

def make_mecab_parser(arg=''):
    try:
        import MeCab
    except ImportError:
        return MeCabProcParser(arg)

    return MeCabParser(arg)

class MeCabParser(object):
    def __init__(self, arg=''):
        model = MeCab.Model_create(arg)
        if model is None:
            raise Exception('Cannot initialize mecab')
        self.model = model
        
    def parse(self, s):
        tagger = self.model.createTagger()
        lattice = self.model.createLattice()
        lattice.set_sentence(s)
        tagger.parse(lattice)
        node = lattice.bos_node()
        morphs = []
        while node:
            if node.surface != '':
                feature = node.feature
                morphs.append({
                    'surface': node.surface,
                    'pos': feature[0:feature.find(',')],
                    'feature': feature,
                })
            node = node.next
        return morphs

class MeCabProcParser(object):
    def __init__(self, command='mecab'):
        self.command = command

    def parse(self, s):
        proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        out = proc.communicate(s)[0]
        morphs = []
        from cStringIO import StringIO
        for l in StringIO(out):
            line = l.strip()
            if line == 'EOS':
                break
            m = re.match(r'(.*)\t(.*)', line)
            if m:
                surface = m.group(1)
                feature = m.group(2)
                pos = feature.split(',')[0]
                morphs.append({
                    'surface': surface,
                    'pos': pos,
                    'feature': feature,
                })

        return morphs
